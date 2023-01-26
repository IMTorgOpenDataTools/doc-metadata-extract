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


def test_create_report():
    template_path = './doc_extract/templates'
    report = Report(logger, template_path)
    html = report.create_report()
    assert html == '<h1>Hello World!</h1>'