#!/usr/bin/env python3
"""
Tests for the main workflow of the application
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import time
import sys
from pathlib import Path

sys.path.append(Path('doc_extract').absolute().as_posix() )
from doc_extract.main import (
    ingest_data,
    modify_and_copy_files,
    create_index_report
)




class Args:
    workflow = None
    input_dir = Path('./tests/demo')


def test_cli_workflow():
    #setup
    start_tm = time.time()
    args = Args()
    args.workflow = 'cli'

    #run
    input_dir, files = ingest_data(args)
    output_dir, docs = modify_and_copy_files(input_dir, files)
    create_index_report(output_dir, docs)
    final_tm = time.time() - start_tm 
    print(f'Final time is {final_tm} sec')
    assert True == True

    #TODO: finally, clean-up dir

def test_api_workflow():
    #setup
    start_tm = time.time()
    args = Args()
    args.workflow = 'api'

    #run
    input_dir, files = ingest_data(args)
    output_dir, docs = modify_and_copy_files(input_dir, files)
    create_index_report(output_dir, docs)
    final_tm = time.time() - start_tm 
    print(f'Final time is {final_tm} sec')
    assert True == True

    #TODO: finally, clean-up dir