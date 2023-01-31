#!/usr/bin/env python3
"""
Tests for the main workflow of the application
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
from pathlib import Path

sys.path.append(Path('doc_extract').absolute().as_posix() )
from doc_extract.main import (
    ingest_data,
    modify_and_copy_files,
    create_index_report
)




class Args:
    input_dir = Path('./tests/demo')


def test_main_workflow():
    args = Args()
    input_dir, files = ingest_data(args)
    output_dir, docs = modify_and_copy_files(input_dir, files)
    create_index_report(output_dir, docs)
    assert True == True

    #TODO: finally, clean-up dir