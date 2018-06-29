from . import PDFReader
from . import ReferenceAcquire
from . import Spider


class RefExtractor:
    def __init__(self, pdf_file_path, pdf_password=None, scholar='google'):
        self.scholar = scholar
        self.pdf = PDFReader.PDFReader(pdf_file_path)
        self.parser = ReferenceAcquire.ReferenceAcq(self.pdf.parse(pdf_password))
        self.records = []

    def extract(self):
        titles = self.parser.get_reference()
        total = len(titles)
        count = 0
        for title in titles:
            self.records.append(Spider.Spider(title, self.scholar).get_bib())
            count += 1
            print('Bib Extracted:%d / %d' % (count, total))
        return self.records
