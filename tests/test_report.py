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
    template_path = './doc_extract/templates'
    template = 'index.html'

    image_path = Path(template_path) / 'static/chart.svg'
    svg_image = load_svg(image_path)

    record_tuples = [     
        DocumentRecord(
            id=1,
            filepath=None,
            filename_original=None,
            filename_modified='Document Title 1',
            file_extension=None,
            filetype=None,
            page_nos=100,
            length_lines=None,
            file_size_mb='30KB',
            date=None,
            reference_number=None,
            title='Document Title 1',
            author=None,
            subject=None,
            toc=None,
            pp_toc='Lorem ipsum dolor sit amet, <br>consectetur adipiscing elit, <br>sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. <br>Ut enim ad minim veniam, <br>quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <br>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. <br>Excepteur sint occaecat cupidatat non proident, <br>sunt in culpa qui officia deserunt mollit anim id est laborum.',
            body='Mr. Green killed Colonel Mustard in the study with the green candlestick.',
            tag_categories=None,
            keywords=None,
            summary=None
            ),
        DocumentRecord(
            id=2,
            filepath=None,
            filename_original=None,
            filename_modified='Document Title 2',
            file_extension=None,
            filetype=None,
            page_nos=200,
            length_lines=None,
            file_size_mb='30KB',
            date=None,
            reference_number=None,
            title='Document Title 2',
            author=None,
            subject=None,
            toc=None,
            pp_toc='Lorem ipsum dolor sit amet, <br>consectetur adipiscing elit, <br>sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. <br>Ut enim ad minim veniam, <br>quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <br>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. <br>Excepteur sint occaecat cupidatat non proident, <br>sunt in culpa qui officia deserunt mollit anim id est laborum.',
            body='Professor Plumb has a green plant in his study',
            tag_categories=None,
            keywords=None,
            summary=None
            )
        ]
    records = [rec._asdict() for rec in record_tuples]
    lunr_index = lunr(
        ref='id', fields=('title', 'body'), documents=records
    )
    template_data = {'records': records,
                     'lunr_index': lunr_index.serialize(),
                     'svg_image': svg_image
                     }
    filepath = './tests/html/index_out.html'

    report = Report(logger, template_path)
    html = report.create_report(template=template, 
                                template_data=template_data
                                )
    report.save_report(html, filepath=filepath)
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