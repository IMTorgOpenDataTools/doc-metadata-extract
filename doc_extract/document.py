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
import itertools

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
            logger.info("TypeError: arg `path` {path} must be of type pathlib.Path")
            raise TypeError
        elif not cond2:
            logger.info(f"arg `path` {path} must be a file")
            raise TypeError
            
        self.filepath = path
        self.filename_original = path.stem
        self.filename_modified = None
        self.file_extension = path.suffix

        self.filetype = None
        self.file_size_mb = None
        self.length_lines = None

        self.filetype, self.file_size_mb = self.determine_file_info(path)
        extractions = self.apply_extraction(logger)
        for k,v in extractions.items():
            setattr(self, k, v)
        self.run_pipeline()
        self.rename_file()

    def determine_file_info(self, path):
        """Determine file system information for the file.

        The format (extension) of the filepath is important 
        to determine what extraction method to use.  Additional
        information is also included.
        """
        if path.suffix in list(self._useable_suffixes.keys()):
            filetype = path.suffix
        else:
            filetype = None
        size_in_mb = int(path.stat().st_size) * 1e-6
        filesize = round(size_in_mb, ndigits=3)
        return filetype, filesize

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
        result['pp_toc'] = self.pretty_print_toc( result['toc'] )
        return result

    def run_pipeline(self):
        """Run nlp pipeline to apply tags.
        
        Get the number of sentences (`length_lines`) for the excerpts made,
        which is based on `utils.MAX_PAGE_EXTRACT`.
        """
        docs = nlp.pipe(self.text)
        docs, gen1 = itertools.tee(docs)
        self.docs = docs
        length_lines = 0
        for doc in gen1:
            length_lines += len(list(doc.sents))
        self.length_lines = length_lines
        return 1

    def rename_file(self):
        """Determine `self.filename_modified` for the new file name."""
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

    def pretty_print_toc(self, toc, file_or_screen='file'):
        """Print table of contents (toc) in human-readable manner."""
        outlines = toc
        if outlines:
            if file_or_screen == 'screen':
                #TODO:for(level,title,dest,a,se) in outlines:
                for(level,title,dest) in outlines:
                    print( ' '.join(title.split(' ')[1:]) )

            elif file_or_screen=='file':              
                outline_lst = []
                for(level,title,dest) in outlines:
                    item = f'{title}'
                    outline_lst.append(item)
                outline_html_str = ('<br>').join(outline_lst)
                return outline_html_str

            else:
                return 0