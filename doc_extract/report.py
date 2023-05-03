#!/usr/bin/env python3
"""
Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from utils import DocumentRecord


class Report:
    """Singleton maintaining functionality for making reports from
    templates.

    Usage:
    template_path = './doc_extract/templates'
    output_filepath = output_dir / template
    report = Report(logger, template_path)
    """

    def __init__(self, logger, template_path):
        """
        
        :param logger(logzero.logger) - log process records
        :param template_path - directory containing jinja2 templates
        
        """
        self.template_path = None
        template_path = Path(template_path)
        if template_path.is_dir():
            self.template_path = template_path
        else:
            logger.info("`template_path` arg must be directory")
            raise TypeError
        
    def create_report(self, template, template_data, output_path=False):
        """Create a report combining template and data.

        :param template - jinja2 template
        :param template_data(dict[str,Document]) - data to fill template
        :return output_from_parsed_template(str) - string formatted html of filled template

        Usage:
        template = 'index.html'
        template_data = {'records': docs}
        html = report.create_report(template=template, 
                                    template_data=template_data
                                    )
        """
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template(template)
        output_from_parsed_template = template.render(template_data)

        if output_path:
            with open(output_path, "w") as fh:
                fh.write(output_from_parsed_template)
            return None
        else:
            return output_from_parsed_template

    def save_report(self, html, filepath):
        """Save the report to file.
        Usage:
        report.save_report(html, filepath=output_filepath)
        """
        with open(filepath, "w") as f:
            f.write(html)