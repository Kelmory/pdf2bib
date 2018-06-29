<<<<<<< HEAD
import math


class Record:
    def __init__(self):
        self.bibtex = None

    def __str__(self):
        return self.bibtex


class ParsedRecord(Record):
    def __init__(self, ref_type, title, authors, year, journal, *kwargs):
        self._type = ref_type
        self._title = title
        self._authors = authors
        self._year = year
        self._journal = journal
        self._extend_info = {}
        for key,value in kwargs:
            self._extend_info[key] = value
        self.tab_len = 4
        self._max_space = self._get_max_space()

    def prettify(self):
        key_value_str = self._single_prettify('title', self._title)
        key_value_str = key_value_str + self._single_prettify('authors', self._authors)
        key_value_str = key_value_str + self._single_prettify('year', self._year)
        key_value_str = key_value_str + self._single_prettify('journal', self._journal)
        for key in self._extend_info:
            key_value_str = key_value_str + self._single_prettify(key, self._extend_info[key])
        bib_item = '@%s{\n%s\n},\n' % (self._type.lower(),key_value_str)
        return bib_item

    def _single_prettify(self, key, value):
        return '%s%s:\t{%s},\n' % (key, self._get_tabs(key), value)

    def _get_tabs(self, key):
        key_len = len(key)
        return int(math.ceil((self._max_space * self.tab_len - key_len) / self.tab_len)) * '\t'

    def _get_max_space(self):
        max_len = 7
        for i in self._extend_info.keys():
            max_len = max(len(i), max_len)
        return int(math.ceil(max_len / self.tab_len))
=======
import math


class Record:
    def __init__(self):
        self.bibtex = None

    def __str__(self):
        return self.bibtex


class ParsedRecord(Record):
    def __init__(self, ref_type, title, authors, year, journal, *kwargs):
        self._type = ref_type
        self._title = title
        self._authors = authors
        self._year = year
        self._journal = journal
        self._extend_info = {}
        for key,value in kwargs:
            self._extend_info[key] = value
        self.tab_len = 4
        self._max_space = self._get_max_space()

    def prettify(self):
        key_value_str = self._single_prettify('title', self._title)
        key_value_str = key_value_str + self._single_prettify('authors', self._authors)
        key_value_str = key_value_str + self._single_prettify('year', self._year)
        key_value_str = key_value_str + self._single_prettify('journal', self._journal)
        for key in self._extend_info:
            key_value_str = key_value_str + self._single_prettify(key, self._extend_info[key])
        bib_item = '@%s{\n%s\n},\n' % (self._type.lower(),key_value_str)
        return bib_item

    def _single_prettify(self, key, value):
        return '%s%s:\t{%s},\n' % (key, self._get_tabs(key), value)

    def _get_tabs(self, key):
        key_len = len(key)
        return int(math.ceil((self._max_space * self.tab_len - key_len) / self.tab_len)) * '\t'

    def _get_max_space(self):
        max_len = 7
        for i in self._extend_info.keys():
            max_len = max(len(i), max_len)
        return int(math.ceil(max_len / self.tab_len))
>>>>>>> 46431f867d190d95d5b4df43f1fa349b9eb11098
