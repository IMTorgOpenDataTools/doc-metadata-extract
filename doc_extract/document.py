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
import shutil

import extractions as ex



class Document:
    """Determine doc type and apply appropriate extractions and transformations.
    
    """
    _useable_suffixes = {'.docx': ex.extract_docx,
                         '.html': ex.extract_html,
                         '.pdf': ex.extract_pdf,
                         '.csv': ex.extract_csv,
                         '.xlsx': ex.extract_xlsx
                        }
    #TODO: word_extensions = [".doc", ".odt", ".rtf", ".docx", ".dotm", ".docm"]
    #TODO: ppt_extensions = [".ppt", ".pptx"]

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
        self.filename_original = path.stem
        self.filename_modified = None
        self.file_extension = path.suffix
        self.filetype = self.determine_filetype(path)
        extractions = self.apply_extraction(logger)
        for k,v in extractions.items():
            setattr(self, k, v)
        self.run_pipeline()
        self.rename_file()

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

    def rename_file(self):
        if self.title:
            self.filename_modified = self.title + self.file_extension
        else:
            self.filename_modified = self.filename_original + self.file_extension
        return 1

    def save_modified_file(self, filepath_modified):
        """Copy the original file with the modified name.
        
        This is the only method not automatically performed on initialization
        because it is making modification outside the object.
        """
        filepath_dst = filepath_modified / self.filename_modified
        shutil.copy(src=self.filepath,
                    dst=filepath_dst
        )
        return 1

    def pretty_print_toc(self):
        outlines = self.toc
        if outlines:
            for(level,title,dest,a,se) in outlines:
                print(' '.join(title.split(' ')[1:])) 