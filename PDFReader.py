<<<<<<< HEAD
from . import Spider

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

import logging
logging.propagate = False
logging.getLogger('pdfminer').setLevel(logging.ERROR)


class PDFReader:
    def __init__(self, _path):
        self._path = _path
        self._online = self.is_online()

    def is_online(self):
        if self._path.find('http') >= 0:
            return True
        else:
            return False

    def parse(self, password=None):
        if not self._online:
            try:
                fp = open(self._path, 'rb')
            except:
                raise FileNotFoundError
        else:
            try:
                fp = Spider(self._path).get_from_url()
            except:
                raise FileNotFoundError

        parser_pdf = PDFParser(fp)
        doc = PDFDocument()
        parser_pdf.set_document(doc)
        doc.set_parser(parser_pdf)

        if password is not None:
            doc.initialize(password)
        else:
            doc.initialize()

        if not doc.is_extractable:
            print('Not extractable.')
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            buffer = []
            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for out in layout:
                    if hasattr(out, "get_text"):
                        if isinstance(out, LTTextBoxHorizontal):
                            buffer.append(out.get_text())
            return buffer
=======
from . import Spider

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

import logging
logging.propagate = False
logging.getLogger('pdfminer').setLevel(logging.ERROR)


class PDFReader:
    def __init__(self, _path):
        self._path = _path
        self._online = self.is_online()

    def is_online(self):
        if self._path.find('http') >= 0:
            return True
        else:
            return False

    def parse(self, password=None):
        if not self._online:
            try:
                fp = open(self._path, 'rb')
            except:
                raise FileNotFoundError
        else:
            try:
                fp = Spider(self._path).get_from_url()
            except:
                raise FileNotFoundError

        parser_pdf = PDFParser(fp)
        doc = PDFDocument()
        parser_pdf.set_document(doc)
        doc.set_parser(parser_pdf)

        if password is not None:
            doc.initialize(password)
        else:
            doc.initialize()

        if not doc.is_extractable:
            print('Not extractable.')
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            buffer = []
            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for out in layout:
                    if hasattr(out, "get_text"):
                        if isinstance(out, LTTextBoxHorizontal):
                            buffer.append(out.get_text())
            return buffer
>>>>>>> 46431f867d190d95d5b4df43f1fa349b9eb11098
