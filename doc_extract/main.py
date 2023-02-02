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
        doc = Document(logger, file)
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

    """
    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    """
    args = parser.parse_args()
    main(args)
    logger.info(f'process completed')
