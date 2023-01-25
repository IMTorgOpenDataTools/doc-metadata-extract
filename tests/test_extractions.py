"""
Tests for Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



import doc_extract.extractions as ex

from pathlib import Path
from logzero import logger
import pytest

class Tmp:
    filepath = 'tests/data/example.docx'


def test_extract_docx():
    obj = Tmp()
    record = ex.extract_docx(obj, logger)
    assert record['title'] == 'Document Title'
    assert len(record['text']) == 7