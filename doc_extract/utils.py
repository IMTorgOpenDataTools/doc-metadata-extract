#!/usr/bin/env python3
"""
Shared utility functions and data
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from faker import Faker

import signal
from collections import namedtuple
from typing import Any
import copy
import inspect

MAX_PAGE_EXTRACT = None
MAX_CONTENT_SIZE = 1e+8    #in bytes => 100MB
ALLOWED_EXTENSIONS = {'.zip'}


# Object storing each Filing's multiple Documents.
#TODO:implement record in this, then xfer Document data to this object, which will be used as input parameters
"""TODO add keys: author, tag_categories, summary
Keys are format, encryption, title, author, subject, keywords, (creator, producer=>author), creationDate, modDate, trapped.
"""
record_attrs = [
        #file indexing
        "id",
        "reference_number",
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
        "title",
        "author",
        "subject",
        "toc",
        "pp_toc",

        "body",
        "clean_body",
        "readability_score",
        "tag_categories",
        "keywords",
        "summary"
]
DocumentBase = namedtuple("DocumentBase", record_attrs)


fake = Faker()
Faker.seed(0)
class DocumentRecord(DocumentBase):
     """Extended functionality of namedtuple."""

     _count = 0
     _inherited_attrs = ['count','index']

     def __new__(cls, **kwargs):
          """Create new DocumentRecord object.  Ensure the 
          record maintains the correct attributes and an 
          original index number.

          Usage::
          empty_doc = DocumentRecord()
          typical_doc = DocumentRecord(title='title', author='name')
          fake_doc = DocumentRecord(id='FAKE')
          """
          idx = 'id'
          base_attrs = record_attrs
          if idx in kwargs.keys():
               if kwargs[idx] == 'FAKE':
                    new_kwargs = cls._create_fake_record(cls)
          else:
               new_kwargs = {}
               for k in base_attrs:
                    if k==idx: 
                         new_kwargs[k] = cls._get_next_index(cls)
                    elif k not in kwargs.keys(): 
                         new_kwargs[k] = None
                    else: 
                         new_kwargs[k] = kwargs[k]
          self = super(DocumentRecord, cls).__new__(cls, **new_kwargs)
          return self
     
     def _get_next_index(cls):
          """Control class index values."""
          original_count = copy.deepcopy(cls._count)
          cls._count = original_count + 1
          return original_count

     def _create_fake_record(cls):
          """Create a realistic but fake record."""
          title = 'Document Title'+str(fake.random_int())
          toc = [str(idx+1) + ') ' + fake.text(max_nb_chars = 20) for idx in range(7)]
          tmp = fake.text(max_nb_chars = 5000)
          body = ' '.join(tmp.split()).replace('\n',' ')
          summary = body[:100]
          record_values = {
               'id': cls._get_next_index(cls),
               'filepath': fake.file_path(),
               'filename_original': fake.file_name(),
               'filename_modified': title,
               'file_extension': fake.file_extension(),
               'filetype': fake.random_choices(elements=('.pdf','docx')),
               'page_nos': fake.random_int(),
               'length_lines': fake.random_int(),
               'file_size_mb': str(fake.random_int())+'KB',
               'date': fake.date_time(),
               'reference_number': fake.random_int(),
               'title': title,
               'author': fake.name(),
               'subject': fake.safe_color_name(),
               'toc': toc,
               'pp_toc': ' <br>'.join(toc),
               'body': body,
               'tag_categories': fake.random_choices(elements=('astronomy','biology','math')),
               'keywords': fake.text(max_nb_chars = 20),
               'summary': summary
          }
          check_attrs = set(record_values.keys()).difference(set(record_attrs))
          if check_attrs: 
               raise TypeError
          return record_values

     def validate_object_attrs(self, target):
          """Validate that an object has the same attributes
          as DocumentRecord.

          TODO: check types also

          :param target - document object
          :return result(dict[str,str]) - which attributes should be added / removed from target
          """
          pairs = inspect.getmembers(target, lambda a:not(inspect.isroutine(a)))
          target_attrs = set( [a[0] for a in pairs if not(a[0].startswith('__') and a[0].endswith('__'))] )
          docrec_attrs = set( self._asdict().keys() )
          docrec_attrs_missing = target_attrs.difference(docrec_attrs)
          target_attrs_missing = docrec_attrs.difference(target_attrs)
          result = {'target_attrs_to_remove': docrec_attrs_missing,
                    'target_attrs_to_add': target_attrs_missing,
                    }
          return result


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