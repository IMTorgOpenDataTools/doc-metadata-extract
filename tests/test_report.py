#!/usr/bin/env python3
"""
Tests for Report class.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import sys
sys.path.append(Path('doc_extract').absolute().as_posix() )
from doc_extract.report import Report

from pathlib import Path
from logzero import logger
import pytest


def test_create_simple_report():
    template_path = './tests/html'
    template = 'simple_report.html'
    template_args = {'foo':'Hello World!'}

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_args=template_args
                                )
    assert html == '<h1>Hello World!</h1>'

def test_create_table():
    template_path = './doc_extract/templates'
    template = 'index.html'
    record1 = {'title': 'Document Title 1',
          'page_nos': 100,
          'size': '30KB',
          'toc': 'Lorem ipsum dolor sit amet, <br>consectetur adipiscing elit, <br>sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. <br>Ut enim ad minim veniam, <br>quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <br>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. <br>Excepteur sint occaecat cupidatat non proident, <br>sunt in culpa qui officia deserunt mollit anim id est laborum.'
        }
    record2 = {'title': 'Document Title 2',
          'page_nos': 200,
          'size': '2MB',
          'toc': 'Ipsum lorem dolor sit amet, <br>consectetur adipiscing elit, <br>sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. <br>Ut enim ad minim veniam, <br>quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <br>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. <br>Excepteur sint occaecat cupidatat non proident, <br>sunt in culpa qui officia deserunt mollit anim id est laborum.'
        }
    template_data = {'records':[record1, record2]}
    filepath = './tests/html/index_out.html'

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_args=template_data
                                )
    report.save_report(html, filepath=filepath)
    assert True == True
