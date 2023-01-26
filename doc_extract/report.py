#!/usr/bin/env python3
"""
Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



from jinja2 import Environment, FileSystemLoader

from pathlib import Path


class Report:
    """TODO
    
    output_path: "./tests/output/my_new_file.html"
    """

    def __init__(self, logger, template_path):
        template_path = Path(template_path)
        if template_path.is_dir():
            self.template_path = template_path
        else:
            logger.info("`template_path` arg must be directory")
            raise TypeError
        
    def create_report(self, output_path=False):
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template('report.html')
        output_from_parsed_template = template.render(foo='Hello World!')

        if output_path:
            with open(output_path, "w") as fh:
                fh.write(output_from_parsed_template)
            return None
        else:
            return output_from_parsed_template