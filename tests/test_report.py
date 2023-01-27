#!/usr/bin/env python3
"""
Tests for Report class.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



from doc_extract.report import Report

from pathlib import Path
from logzero import logger
import pytest


def test_create_simple_report():
    template_path = './tests/data'
    template = 'simple_report.html'
    template_args = {'foo':'Hello World!'}

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_args=template_args
                                )
    assert html == '<h1>Hello World!</h1>'

def test_create_table():
    template_path = './doc_extract/templates'
    template = 'table.html'
    template_args = {'sec1':'YoMama',
                     'sec2':'YoMamamama',
                     'sec3':'YoMamamamamammaa',
                    }
    filepath = './tests/data/index_out.html'

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_args=template_args
                                )
    report.save_report(html, filepath=filepath)
    assert True == True
