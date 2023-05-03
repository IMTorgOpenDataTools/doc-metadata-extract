#!/usr/bin/env python3
"""
Shared utility functions and data
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import signal
from collections import namedtuple

MAX_PAGE_EXTRACT = None


# Object storing each Filing's multiple Documents.
#TODO:implement record in this, then xfer Document data to this object, which will be used as input parameters
DocumentRecord = namedtuple(
    "DocumentRecord",
    [
        #file indexing
        "id",
        "filepath",
        "filename_original",
        "filename_modified",

        #raw
        "file_extension",
        "filetype",
        "page_nos",
        "length_lines",
        "file_size_mb",
        "date",

        #inferred / searchable
        "reference_number",
        "title",
        "author",
        "subject",
        "toc",
        "pp_toc",

        "body",
        "tag_categories",
        "keywords",
        "summary"
    ]
)


"""TODO add keys: author, tag_categories, summary
Keys are format, encryption, title, author, subject, keywords, (creator, producer=>author), creationDate, modDate, trapped.


        DocumentRecord(
            id=1,
            filepath=None,
            filename_original=None,
            filename_modified=None,
            file_extension=None,
            filetype=None,
            page_nos=None,
            length_lines=None,
            file_size_mb=None,
            date=None,
            reference_number=None,
            title=None,
            author=None,
            subject=None,
            toc=None,
            pp_toc=None
            body=None,
            tag_categories=None,
            keywords=None,
            summary=None
            )
"""


class TestDocument:
     """Singleton of functionality for validating and 
     testing Documents."""

     def __init__(self):
          pass
     
     def validate_object_keys(self):
          pass
     
     def validate_object_attrs(self):
          pass
     
     def create_named_tuple(self):
          record = DocumentRecord(
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
                  )
          return record
     
     def create_document_objects(self):
          pass


class timeout:
  """Timeout function after duration of seconds
  
  This uses `signal` and so is only useable on linux.
  
  Usage:
  with timeout(seconds=3):
    time.sleep(4)
  """
  def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
  def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
  def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
  def __exit__(self, type, value, traceback):
        signal.alarm(0)


def load_svg(filepath):
     """Load svg image from filepath."""
     image = ''
     with open(filepath, 'r') as f:
          image = f.read()
     return image