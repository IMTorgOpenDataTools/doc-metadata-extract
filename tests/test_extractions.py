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




def test_extract_docx():
    #TODO: improve convert .docx to .pdf
    #filepath_str = 'tests/data/example.docx', 'Document Title', 7
    filepath_str = 'tests/data/IJSRP-paper-submission-format-single-column.docx'
    class Tmp:
        filepath = Path(filepath_str)
    obj = Tmp()

    record = ex.extract_docx(obj, logger)
    assert record['title'] == 'Document Title'
    assert len(record['text']) == 7

def test_extract_html():
    filepath_str = 'tests/data/Research Articles in Simplified HTML.html'
    #TODO: filepath_str = 'tests/data/Research Articles in Simplified HTML with CSS.html'
    class Tmp:
        filepath = Path(filepath_str)
    obj = Tmp()
    record = ex.extract_html(obj, logger)
    assert record['title'] == 'Abstract'
    assert record['page_nos'] == 18

def test_extract_pdf():
    filepath_str = 'tests/demo/cs_nlp_2301.09640.pdf'
    class Tmp:
        filepath = Path(filepath_str)
    obj = Tmp()
    record = ex.extract_pdf(obj, logger)
    assert record['title'] == 'Weakly-Supervised Questions for Zero-Shot Relation Extraction'
    assert record['page_nos'] == 12