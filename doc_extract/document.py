#!/usr/bin/env python3
"""
Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import spacy
nlp = spacy.load("en_core_web_sm")

from pathlib import Path, PosixPath


from doc_extract import extractions as ex



class Document:
    """Determine doc type and apply appropriate extractions and transformations.
    
    """
    _useable_suffixes = {'.docx': ex.extract_docx,
                         '.html': ex.extract_html,
                         '.pdf': ex.extract_pdf,
                         '.csv': ex.extract_csv,
                         '.xlsx': ex.extract_xlsx
                        }

    def __init__(self, logger, path):
        cond1 = type(path) == PosixPath
        cond2 = path.is_file()
        if not cond1:
            logger.info("TypeError: arg `path` must be of type pathlib.Path")
            raise TypeError
        elif not cond2:
            logger.info("arg `path` must be a file")
            raise TypeError
            
        self.filepath = path
        self.filetype = self.determine_filetype(path)
        extractions = self.apply_extraction(logger)
        for k,v in extractions.items():
            setattr(self, k, v)
        self.run_pipeline()

    def determine_filetype(self, path):
        """Determine the format of the filepath."""
        if path.suffix in list(self._useable_suffixes.keys()):
            result = path.suffix
        else:
            result = None
        return result

    def apply_extraction(self, logger):
        """Apply extractions appropriate for the format.

        Don't throw exception if not an available 
        filetype.  Instead, fail gracefully with result
        of only None values.
        """
        if self.filetype in self._useable_suffixes:
            fun_call = self._useable_suffixes[self.filetype]
            result = (fun_call)(self, logger)
        else:
            logger.info("filetype (extension) is not one of the useable suffixes")
            result = ex.record
        return result

    def run_pipeline(self):
        self.docs = nlp.pipe(self.text)