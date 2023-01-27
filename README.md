# Document Metadata Extract

This project extracts metadata from a document to index it for quick review.


## Graphical Depict Text

* what manageble number (3-6) of topics are overlapping across sources?  => topic modeling
* how can each source be located with respect to each topic?  => network attraction graph
* 



## TODO

* continue with demo/*.pdf
* finish main.py workflow with index.html
* add table to index.html
* deploy to lsf





### docx to pdf

There are different options:

* libreoffice: `cd /DIRECTORY/WITH/FILE/IN && libreoffice --headless --convert-to html 'FILE.docx' && pandoc 'FILE.html' -o 'FILE.pdf'`, [ref](https://unix.stackexchange.com/questions/105584/convert-a-docx-to-a-pdf-with-pandoc)
* pandoc: `pandoc --from docx --to latex` then compile latex to pdf, [ref](https://pandoc.org/try/)
* docx2python: project may be useful, also, [ref](https://github.com/ShayHill/docx2python)