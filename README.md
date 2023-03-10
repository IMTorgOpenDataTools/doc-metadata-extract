# Document Metadata Extract

This project extracts metadata from files within a directory and returns an interactive html index describing the files.


## Data and Representation

Collected file metadata include:

* individual file, raw data: title, authors, toc, size, sentences
* individual file, aggregated data: topics, key words / phrases
* collective directory, comparison data: similarity with others, N-topics and relevance to each topic, ...

Data can graphically displayed:

* what manageble number (3-6) of topics are overlapping across sources?  => topic modeling
* how can each source be located with respect to each topic?  => network attraction graph
* ...


## Run

Add the event file path to the `doc_extract/main.py:trigger_file`

`pipenv run python doc_extract/main.py ./tests/demo/ -tf ./tests/RUN.txt`



## TODO

* ~~continue with demo/*.pdf
* ~~add table to index.html [ref](https://codepen.io/jopico/pen/kyRprJ)
* ~~finish main.py workflow with index.html
* ~~deploy to lsf
* ~~input files from directory
* ~~it is slow because it uses too many pages
* ~~make faster
* ~~rec.name is not available for original name
* ~~size and other attributes should be added
* logs




### docx to pdf

There are different options:

* libreoffice: `cd /DIRECTORY/WITH/FILE/IN && libreoffice --headless --convert-to html 'FILE.docx' && pandoc 'FILE.html' -o 'FILE.pdf'`, [ref](https://unix.stackexchange.com/questions/105584/convert-a-docx-to-a-pdf-with-pandoc)
* pandoc: `pandoc --from docx --to latex` then compile latex to pdf, [ref](https://pandoc.org/try/)
* docx2python: project may be useful, also, [ref](https://github.com/ShayHill/docx2python)