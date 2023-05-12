#!/usr/bin/env python3
"""
API setup
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from pathlib import Path

from doc_extract.utils import (
    MAX_CONTENT_SIZE, 
    ALLOWED_EXTENSIONS
)





class WebAPI:
    """Web API workflow.
    
    Usage::
    upload_foldier = './tests/out'
    template_dir = './doc_extract/templates'
    api = WebAPI(upload_foldier, template_dir)
    """

    def __init__(self, upload_foldier, template_dir):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = upload_foldier
        self.app.config['MAX_CONTENT_PATH'] = MAX_CONTENT_SIZE
        self.app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
        self.template_dir = Path(template_dir)

    #setup
    def configs(self, **configs):
        """Add all k:v configs."""
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        """Add endpoint with args."""
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)