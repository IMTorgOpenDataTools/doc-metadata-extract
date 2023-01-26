#!/usr/bin/env python3
"""
Tests for the main workflow of the application
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from pathlib import Path

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
    docs = modify_and_copy_files(input_dir, files)
    assert len(docs)>0

    #TODO: finally, clean-up dir