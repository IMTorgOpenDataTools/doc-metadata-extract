#!/usr/bin/env python3
"""
Extraction functions for each file type to be used with Document class

Notes on getting text:
* assume docs are max 100 pages - only get N bytes of string to conserve memory
* `text_lst` itesms should be in batches, such as doc pages or paragraphs (don't mess up sentenceizer)
* `docs = spacy.pipe(text_lst, n_process=-1)`   #as many processes as CPUs
* resulting docs is a generator, but return as list `list(docs)`, currently
* then Document performs text processing

TODO:
* convert all file types to pdf, then extract using pdf.miner
* limit retrieval to N excerpts
* use optimal storage: `from collections import namedtuple`   #ref: https://stackoverflow.com/questions/1336791/dictionary-vs-object-which-is-more-efficient-and-why
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



import pandas as pd

import bs4
from bs4.element import Comment

import docx

import pypdf
import pdftitle                                                                 #uses pdfminer
from pdfminer.high_level import extract_text as pdf_extract_text                #uses pdfminer.six, problem TODO???
from pdfminer.high_level import extract_pages as pdf_extract_pages
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import fitz




record = {'title': None,
          'page_nos': None,
          'length_lines': None,
          'toc': None,
          'text': None
        }

"""add keys: author, tag_categories, toc_chapter_headers, summary"""

def get_title(txt):
    pass

def clean_text(txt):
    if type(txt) is list:
        combined_txt = ('.').join(txt)
        return combined_txt.replace('.','.  ').replace('\n',' ')
    elif type(txt) is str:
        txts = txt.split('.\n')
        txts = [txt.replace('-\n','').replace('\n',' ') for txt in txts]
        return txts
    else:
        return txt




def extract_docx(self, logger):
    """Extract from docx filetype.
    
    'text': excerpts.paragraphs
    """
    try:
        excerpts = docx.Document(self.filepath)
    except:
        logger.info("TypeError: document not of type `.docx`")
        return None
    txt = [par.text for par in excerpts.paragraphs]

    record['title'] = excerpts.paragraphs[0].text     #<<< get_title(txt)
    record['length_lines'] = len( clean_text(txt).split('.') )
    record['text'] = txt
    return record


def extract_html(self, logger):
    """Extract for html filetype.
    
    'text': visible text
    """

    #ref: https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    with open(self.filepath.__str__(), 'r') as f:
        html = f.readlines()
    clean_html = ('').join(html).replace('\n','')
    try:
        excerpts = bs4.BeautifulSoup(clean_html, 'html.parser')
    except:
        logger.info("TypeError: document not of type `.html`")
        return None
    txt = text_from_html(excerpts)

    record['title'] = excerpts.find('title').text
    record['text'] = txt
    return record


def extract_pdf(self, logger):
    """Extract from pdf filetype.
    
    'text': pages
    """
    def get_title(title):
        if not title:
            with open(self.filepath.__str__(), 'rb') as f:
                pdfReader = pypdf.PdfReader(f)
                first_str = len(excerpts[0])
                if pdfReader.metadata['/Title']:
                    title = pdfReader.metadata['/Title']
                elif first_str>0 and first_str<100:
                    title = first_str
                else:
                    pass
        return title

    def get_toc():
        outlines = None
        with open(self.filepath.__str__(), 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            # Get the outlines of the document.
            try:
                outlines = list(document.get_outlines())
            except:
                pass
        if not outlines:
            doc = fitz.open(self.filepath.__str__())
            tmp = doc.get_toc()
            outlines = tmp if tmp != [] else None
        return outlines


    title = None
    try:
        title = pdftitle.get_title_from_file(self.filepath.__str__())
    except Exception:
        logger.info("`pdftitle` module threw error")
        pass
    raw_text = pdf_extract_text(self.filepath.__str__())
    excerpts = clean_text(raw_text)
    pages_gen = pdf_extract_pages(self.filepath.__str__())
    page_nos = sum(1 for x in pages_gen)

    record['title'] = get_title(title)
    record['page_nos'] = page_nos
    record['toc'] = get_toc()
    record['text'] = excerpts

    return record


def extract_csv(self, logger):
    df = pd.read_csv(self.filepath.__str__(), 
                    nrows=1
                    )
    record['title'] = df.columns[0].replace('\n','')
    return record


def extract_xlsx(self, logger):
    sheets = pd.ExcelFile(self.filepath.__str__()).sheet_names
    df = pd.read_excel(self.filepath.__str__(), 
                        sheet_name=sheets[0], 
                        nrows=1
                        )

    record['title'] = df.columns[0].replace('\n','')
    return record