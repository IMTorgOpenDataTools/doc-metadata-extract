# Document Metadata Extract

This project extracts metadata from files within a directory and returns a single, interactive html index of file descriptions.  Rather than opening and reviewing files, individually, the interactive index is intended to be a portable, single-source of reference for the documents.

This is useful when performing manual information extraction with large numbers of documents.  The following helps explain the type of questions it answers.

![Information Extraction Framework](./docs/IE_framework.jpg)


## Data and Representation

File formats available for data extraction:

* pdf
* pdf of images (typically ppt)
* TODO: docx, xlsx, ppt, ...

Collected file metadata include:

* individual file, raw data: title, authors, toc, size, sentences
* individual file, aggregated data: topics, key words / phrases, internal wordnet
* collective directory, comparison data: similarity with others, N-topics and relevance to each topic, ...

Data can be graphically displayed:

* what manageble number (3-6) of topics are overlapping across sources?  => topic modeling
* how can each source be located with respect to each topic?  => network attraction graph
* ...



## Run

This can be run using multiple methods

* commandline: `python3 -m doc_extract --input_dir ./tests/demo/ --output_dir ./tests/demo_mod/ --output_format html`
* docker: `TODO >>> python3 docker_run.py tests/resources/blog_test-hugo_blog.ipynb  ./ `
* aws lambda container: ``
* development: `pipenv run python doc_extract/main.py ./tests/demo/ -tf ./tests/RUN.txt --output html`


## TODO

### Requirements

_workflow_
* ~~continue with demo/*.pdf
* ~~add table to index.html [ref](https://codepen.io/jopico/pen/kyRprJ)
* ~~finish main.py workflow with index.html
* ~~deploy to lsf
* ~~input files from directory
* ~~it is slow because it uses too many pages
* ~~make faster
* ~~rec.name is not available for original name
* ~~size and other attributes should be added
* ~~build lunr index and add full text
* >separate text (then index) into smaller pieces (section, page) to optimize lunr search
* >extract unique file key (if available)
* >extract folder structure
* ocr docs of images, such as ppt slides

_commandline_
* logs
* explore indv aggregated data
* move triggerfile to external
* add arguments
* add outputs
* run via cmdln as module

_frontend_
* ~~search 
  - ~~lunr index
  - highlight specific text
* ~~use `bootstrap-vue` for child details row
* add readability score column
* change columns to: Details,Id,Ref,Title,Folder Structure, Original File Name, ...
* create score column with results from search, and sort rows by it
* add multiple results and accompanying sections into row.snippets
* separate each template into components for better testing
* separate out css
* sort by folder structure and key words columns, [ref](https://www.w3schools.com/howto/howto_js_sort_table.asp)
* export selected references to xlsx, [ref](https://sheetjs.com/demo/table)
* help modal and tooltips
* textnets selectable svg modal

_design considerations_
* single webpack on html file
* tests for maximum data html file can hold
* convert into Singletons: Report, WebAPI
* >deploy with flask


### Long-term

This prototype should be separated by scope.  The `doc-metadata-extract` should focus soley on extracting raw data from different document formats (`document.py`,`extractions.py`).  This requires combining many different modules and algorithms.  In contrast, a serverless deployment should be created to perform API routing, data aggregation, and reporting functionality.


### Word files

For docx-to-pdf there are different options:

* libreoffice: `cd /DIRECTORY/WITH/FILE/IN && libreoffice --headless --convert-to html 'FILE.docx' && pandoc 'FILE.html' -o 'FILE.pdf'`, [ref](https://unix.stackexchange.com/questions/105584/convert-a-docx-to-a-pdf-with-pandoc)
* pandoc: `pandoc --from docx --to latex` then compile latex to pdf, [ref](https://pandoc.org/try/)
* docx2python: project may be useful, also, [ref](https://github.com/ShayHill/docx2python)