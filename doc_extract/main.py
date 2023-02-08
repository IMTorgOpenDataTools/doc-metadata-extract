#!/usr/bin/env python3
"""
Module Docstring

Workflow:
* input data
* get Doc for each file
* rename file where possible
* create html index
* output to folder
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import time
import argparse
import logzero
from logzero import logger
from pathlib import Path

from document import Document
from report import Report


logging_dir = './logs/process.log'
# logging
logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
logzero.logfile(logging_dir, maxBytes=1000000, backupCount=3)            #set rotating log file
logger.info('logger created, constants initialized')




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
    output_dir = root_dir / Path( input_dir.name.__str__() + '_mod' )
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

def create_index_report(output_dir, docs):
    template_path = './doc_extract/templates'
    template = 'index.html'
    template_data = {'records': docs}
    output_filepath = output_dir / template

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_args=template_data
                                )
    report.save_report(html, filepath=output_filepath)



def main(args):
    """ Main entry point of the app """
    logger.info(f'process initiated with arguments: {args}')
    if args.trigger_file:
        remove_trigger_file(args.trigger_file) 
    input_dir, files = ingest_data(args)
    logger.info(f'data ingested from input directory: {input_dir}')
    output_dir, docs = modify_and_copy_files(input_dir, files)
    logger.info(f'data ingested from input directory: {output_dir}')
    create_index_report(output_dir, docs)
    logger.info(f'index report created')
    
            



        





if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    
    # Required positional argument
    parser.add_argument("input_dir", help="Input directory containing files")

    # Optional argument flag which defaults to False
    parser.add_argument("-tf", "--trigger_file", default=False, help="File used to trigger even")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
    logger.info(f'process completed')
