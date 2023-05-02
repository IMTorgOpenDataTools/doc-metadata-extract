"""
Tests for Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import time
import sys
from pathlib import Path
sys.path.append(Path('doc_extract').absolute().as_posix() )
import doc_extract.extractions as ex


from logzero import logger
import pytest




def test_extract_docx():
    #TODO: improve convert .docx to .pdf
    #TODO: this fails because title includes to much: 'record['title']  "Title for paper submitted to International Journal of Scientific and Research PublicationsFirst Author*, Second Author**, Th....
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
    start_tm = time.time()
    filepath_str = 'tests/demo/cs_nlp_2301.09640.pdf'    #3.3sec, 21sec, 0.65sec
    #filepath_str = 'tests/demo/nuclear_2201.00276.pdf'    #3.8sec, 1.35sec
    class Tmp:
        filepath = Path(filepath_str)
    obj = Tmp()
    record = ex.extract_pdf(obj, logger)
    final_tm = time.time() - start_tm 
    print(f'Final time is {final_tm} sec')
    #assert True == True
    assert record['title'] == 'Weakly-Supervised Questions for Zero-Shot Relation Extraction'
    assert record['page_nos'] == 12