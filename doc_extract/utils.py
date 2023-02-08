#!/usr/bin/env python3
"""
Shared utility functions and data
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import signal

MAX_PAGE_EXTRACT = None

record = {'title': None,
          'author': None,
          'subject': None,
          'keywords': None,
          'date': None,

          'page_nos': None,
          'length_lines': None,
          'toc': None,
          'text': None
        }

"""TODO add keys: author, tag_categories, summary
Keys are format, encryption, title, author, subject, keywords, (creator, producer=>author), creationDate, modDate, trapped.
"""



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