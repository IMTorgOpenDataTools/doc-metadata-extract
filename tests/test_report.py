#!/usr/bin/env python3
"""
Tests for Report class.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from lunr import lunr

import sys
from pathlib import Path
sys.path.append(Path('doc_extract').absolute().as_posix() )
from doc_extract.report import Report
from doc_extract.utils import DocumentRecord, load_svg

from logzero import logger
import pytest


def test_create_simple_report():
    template_path = './tests/html'
    template = 'simple_report.html'
    template_args = {'foo':'Hello World!'}

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_data=template_args
                                )
    assert html == '<h1>Hello World!</h1>'

def test_create_filled_report():
    output_filepath = './tests/RESULT/index_out.html'
    template_path = './doc_extract/templates'
    template = 'index.html'
    image_path = Path(template_path) / 'static/chart.svg'
    svg_image = load_svg(image_path)
    number_of_records = 5

    docs = [DocumentRecord(id='FAKE') for i in range(number_of_records )] 
    records = []  
    for rec in docs:
        rec_dict = rec._asdict()
        rec_dict_str = {k:str(v) for k,v in rec_dict.items()}
        records.append(rec_dict_str )
    lunr_index = lunr(
        ref='id', fields=('title', 'body'), documents=records
    )
    template_data = {'records': records,
                     'lunr_index': lunr_index.serialize(),
                     'svg_image': svg_image
                     }
    

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_data=template_data
                                )
    report.save_report(html, filepath=output_filepath)
    assert True == True


def test_vue():
    template_path = './doc_extract/templates'
    template = 'test.html'
    template_data = {}
    filepath = './tests/html/index_out.html'

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_data=template_data
                                )
    report.save_report(html, filepath=filepath)
    assert True == True