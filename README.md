# PDF2BIB
These scripts are wriiten for extracting references to bibtex from pdf articles.

## Requirements
* Python: 3.5 & above.
* Packages: requests, pdfminer3k, bs4.

## How to Use

### Structure
This package is primarily made up with 4 classes.
* **PDFReader**, reads pdf and returns raw text with `parse(password)`, the password is an alternative option which is `None` in default. When initializing a pdf reader, a path/URL is needed.
* **ReferenceAcquire**, deal with raw texts, get the references with `get_reference()`.
* **Spider**, use scholar engines to fetch complete bibtex records with `get_bib()`. When initializing a spider, a title and a scholar engine name are required, currently supported engines are [bing](https://cn.bing.com/academic), [google](https://scholar.google.com/) and [dblp](http://dblp.uni-trier.de/search).
* **Record**, contains a bibtex record, can use *ParsedRecord()* in substitute.

### Demo
See how to use directly in [demo.py](/demo.py).

## Further works

### Current known problems
* Can be failed to get bibtexs when title is too general.
* Bing and Google engine are not working properly.
* Can only work with articles using **LNCS** template.

### Further Improvements
* To fix engine problems.
* Considering adding offline mode which parse the pdf directly to bibtexs.
* To support more templates.
* To use multi-thread from faster processing.
