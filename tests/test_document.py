#!/usr/bin/env python3
"""
Tests for Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import sys
from pathlib import Path
sys.path.append(Path('doc_extract').absolute().as_posix() )
from doc_extract.document import Document


from logzero import logger
import pytest


def test_document_creation_fail():
    test_file = Path('tests/data/no_file.docx')
    with pytest.raises(Exception) as e_info:
        doc = Document(logger, test_file)

def test_document_determine_filetype_fail():
    """Filetypes that fail: .doc, .rtf, .tif, .docm, .dot"""
    test_file = Path('tests/data/unavailable_extension.doc')
    doc = Document(logger, test_file)
    assert doc.title == None

def test_document_extraction():
    """TODO: create separate tests using pytest."""
    lst = { '.docx': ['tests/data/example.docx', 'Document Title'],
            '.html': ['tests/data/example.html', 'The Website Title'],
            '.pdf': ['tests/data/example.pdf', 'The Website Title'],
            '.csv': ['tests/data/example.csv', 'Document Title'],
            '.xlsx': ['tests/data/example.xlsx', 'Document Title'],
            }
    for k,v in lst.items():
        filepath = v[0]
        title = v[1]
        test_file = Path(filepath)
        doc = Document(logger, test_file)
        assert doc.title == title