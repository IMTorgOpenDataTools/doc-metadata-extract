#!/usr/bin/env python3
"""
Main entrypoint
Select either CLI or API

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from api import WebAPI
from document import Document
from report import Report
from utils import load_svg

from lunr import lunr
from flask import render_template, request
from werkzeug.utils import secure_filename

import ast
import json
import time
import argparse
from pathlib import Path
import logzero
from logzero import logger

logging_dir = './logs/process.log'
# logging
logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
logzero.logfile(logging_dir, maxBytes=1000000, backupCount=3)            #set rotating log file
logger.info('logger created, constants initialized')



# cli
def remove_trigger_file(file_path):
    trigger_file = file_path
    trigger_path = Path(trigger_file)
    trigger_path.unlink()

def ingest_data(args):
    input_dir = Path(args.input_dir)
    files = [x for x in input_dir.glob('**/*') if x.is_file()]
    if not input_dir.is_dir() or len(files)==0:
        logger.info(f"fail: {input_dir} not a directory, or it is empty of files")
        raise TypeError
    return input_dir, files

def modify_and_copy_files(input_dir, files):
    root_dir = input_dir.parent
    output_dir = root_dir / Path( input_dir.name.__str__() + '_RESULT' )
    if output_dir.is_dir():
        logger.info(f"fail: {output_dir} already exists")
        raise TypeError
    else:
        output_dir.mkdir(parents=True, exist_ok=False)

    docs = []
    for file in files:
        start_tm = time.time()
        doc = Document(logger, file)
        end_tm = time.time()
        logger.info(f'Document {file} created in: {end_tm-start_tm}sec')
        doc.save_modified_file(filepath_modified=output_dir)
        docs.append(doc)

    return output_dir, docs

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True
def enforce_json_compliant_string(rec_dict_str):
    rec_dict_str['body'] = rec_dict_str['body'].replace('"','')
    """
    json_str = json.dumps(rec_dict_str)
    fix1 = json_str.replace('"','')    #.replace("\'","")#.replace('\"','')
    fix2 = ast.literal_eval(fix1)
    fix3 = json.loads(json.dumps(fix2))
    """
    return rec_dict_str

def create_index_report(output_dir, docs):
    template = 'index.html'
    output_filepath = output_dir / template
    template_path = './doc_extract/templates'
    image_path = Path(template_path) / 'static/chart.svg'
    svg_image = load_svg(image_path)

    records = []  
    for idx,rec in enumerate(docs):
        rec_dict = rec._asdict()
        rec_dict['id'] = str(idx)
        rec_dict_str = {k:str(v) for k,v in rec_dict.items()}           #TODO:NOTE> all values converted to string before populating index
        enforce_json_compliant = enforce_json_compliant_string(rec_dict_str)
        records.append(enforce_json_compliant)
    lunr_index = lunr(
        ref='id', fields=('title', 'body'), documents=records
        )
    template_data = {'records': records,
                     'lunr_index': lunr_index.serialize(),
                     'svg_image': svg_image
                     }
    
    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_data=template_data
                                )
    report.save_report(html, filepath=output_filepath)

def run_cli(args, logger):
    """
    Workflow:
    * input data
    * get Doc for each file
    * rename file where possible
    * create html index
    * output to folder
    """
    if args.trigger_file:
        remove_trigger_file(args.trigger_file) 
    input_dir, files = ingest_data(args)
    logger.info(f'data ingested from input directory: {input_dir}')
    output_dir, docs = modify_and_copy_files(input_dir, files)
    logger.info(f'data ingested from input directory: {output_dir}')
    create_index_report(output_dir, docs)
    logger.info(f'index report created')


# api
def upload_page(app):
   """Serve user page.
   @app.route('/upload')
   """
   upload_path = app.template_dir / 'upload.html'
   return render_template(upload_path)

def file_uploader(app):
   """Accept uploaded (zip) files.
   @app.route('/uploader', methods = ['GET', 'POST'])
   """
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully' 
     
def run_api(args, logger, **kwargs):
    """Run the web api.
    
    """
    upload_foldier = args.input_dir
    template_dir = './doc_extract/templates'
    api = WebAPI(upload_foldier, template_dir)

    api.add_endpoint('/upload', 'upload', upload_page(api), methods=['GET'])
    api.add_endpoint('/uploader', 'uploader', file_uploader(api), methods=['POST'])
    api.run(**kwargs)



def main(args):
    """ Main entry point of the app """
    logger.info(f'process initiated with arguments: {args}')
    if args.workflow == 'webapi':
        run_api(args, logger)
    elif args.workflow == 'cli':
        run_cli(args, logger)
    else:
        raise TypeError
    
            



        





if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    # Required positional arguments
    parser.add_argument(
        "workflow", 
        choices=['webapi','cli'], 
        help="Select program workflow: <webapi> or <cli>."
        )
    parser.add_argument("input_dir", 
        type=str, 
        help="""Input directory where: i) files will be uploaded (webapp)
                or, ii) containing files to be processed (cli)."""
        )

    # Optional argument flag which defaults to False
    parser.add_argument("-tf", 
                        "--trigger_file", 
                        default=False, 
                        help="File used to trigger event, if needed."
                        )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__)
        )

    args = parser.parse_args()
    main(args)
    logger.info(f'process completed')
