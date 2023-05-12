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
    _record_attrs = [
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
    #TODO: word_extensions = [".doc", ".odt", ".rtf", ".docx", ".dotm", ".docm"]
    #TODO: ppt_extensions = [".ppt", ".pptx"]
    #TODO: initialize all attributes before running methods

    def __init__(self, logger, path):
        cond1 = type(path) == PosixPath
        cond2 = path.is_file()
        if not cond1:
            logger.info(f"TypeError: arg `path` {path} must be of type pathlib.Path")
            raise TypeError
        elif not cond2:
            logger.info(f"arg `path` {path} must be a file")
            raise TypeError
        
        [setattr(self, key, None) for key in self._record_attrs]
        #file indexing
        self.filepath = path
        self.filename_original = path.stem
        self.file_extension = path.suffix
        self.docs = None            #TODO:spacy output not currently used

        self.filetype, self.file_size_mb = self.determine_file_info(path)
        extractions = self.run_extraction_pipeline(logger)
        if self.filetype:
            for k,v in extractions.items():
                if hasattr(self, k):
                    if not getattr(self,k):
                        setattr(self, k, v)
            if self.body:
                self.run_spacy_pipeline(body = self.body)
            self.rename_file()
        missing_attr = self.get_missing_attributes()
        cnt = missing_attr.__len__()
        logger.info(f"Document `{self.filename_original}` populated with {cnt} missing (None) attributes: {missing_attr}")

    def _asdict(self):
        """Return dict of attributes."""
        result = {}
        for attr in self._record_attrs:
            val = getattr(self, attr)
            result[attr] = val
        return result

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

    def run_extraction_pipeline(self, logger):
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

    def run_spacy_pipeline(self, body):
        """Run nlp pipeline to apply tags.
        
        Get the number of sentences (`length_lines`) for the excerpts made,
        which is based on `utils.MAX_PAGE_EXTRACT`.
        """
        docs = nlp.pipe(body)
        docs, gen1 = itertools.tee(docs)
        self.docs = docs
        length_lines = 0
        for doc in gen1:
            length_lines += len(list(doc.sents))
        self.length_lines = length_lines
        return 1

    def rename_file(self):
        """Determine `self.filename_modified` for the new file name."""
        file_extension = '' if self.file_extension == None else self.file_extension
        if self.title:
            self.filename_modified = self.title + file_extension
        else:
            self.filename_modified = self.filename_original + file_extension
        return 1

    def get_missing_attributes(self):
        """Count the number of attributes not populated after initialization
        pipelines are run."""
        result = {}
        missing = []
        for attr in self._record_attrs:
            val = getattr(self, attr)
            result[attr] = val
            if val == None: 
                missing.append(attr)
        return missing

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