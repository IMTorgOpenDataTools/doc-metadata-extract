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
from doc_extract.utils import DocumentRecord


from logzero import logger
import pytest


def test_document_attributes():
    test_file = Path('tests/data/example.pdf')
    doc = Document(logger, test_file)
    docrec = DocumentRecord()
    result = docrec.validate_object_attrs(doc)
    assert list(result) == ['target_attrs_to_remove', 'target_attrs_to_add']

def test_document_populated():
    test_file = Path('tests/demo/econ_2301.00410.pdf')
    doc = Document(logger, test_file)
    docrec = DocumentRecord()
    result = docrec.validate_object_attrs(doc)
    check1 = result['target_attrs_to_remove'] == {'_useable_suffixes', 'docs', '_record_attrs'}
    check2 = not bool(result['target_attrs_to_add'])
    check3 = doc.get_missing_attributes() == ['reference_number', 'tag_categories', 'summary']
    assert not False in [check1, check2, check3]

def test_document_creation_fail():
    test_file = Path('tests/data/no_file.docx')
    with pytest.raises(Exception) as e_info:
        doc = Document(logger, test_file)
    assert type(e_info) == pytest.ExceptionInfo

def test_document_determine_filetype_fail():
    """Filetypes that fail: .doc, .rtf, .tif, .docm, .dot"""
    test_file = Path('tests/data/unavailable_extension.doc')
    doc = Document(logger, test_file)
    assert hasattr(doc, 'title') == False

def test_document_extraction():
    """TODO: create separate tests using pytest."""
    #TODO:currently these fail to capture actual title
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
        assert hasattr(doc, 'title') == True