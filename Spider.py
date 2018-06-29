<<<<<<< HEAD
import requests
import urllib.parse as parse
from bs4 import BeautifulSoup
from . import Record

requests.packages.urllib3.disable_warnings()


# Get one reference information at a time
class Spider:
    ip_list = ['127.0.0.1:8087', '127.0.0.1:8086']
    user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                  'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                  'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                  'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    proxies = {'http': '127.0.0.1:8087',
               'https': '127.0.0.1:8087'}
    scholar_dict = {
        'google'    :{'search':'https://scholar.google.com/scholar?hl=en&q=',
                       'tag_name':'div',
                       'class_name':'gs_r gs_or gs_scl',
                       'title_tag':'h3',
                       'title_class':'',
                       'bib_text':'pre',
                      },
        'bing'      :{'search':'https://cn.bing.com/academic/search?q=',
                       'tag_name':'li',
                       'class_name':'aca_algo',
                       'title_tag': 'h2',
                       'title_class':'',
                       'bib_text':'pre',
                      },
        'dblp'      :{'search':'https://dblp.uni-trier.de/search?q=',
                       'tag_name':'li',
                       'class_name':'entry',
                       'title_tag': 'span',
                       'title_class':'title',
                       'bib_text':'pre',
                      },
    }

    def __init__(self, title, scholar):
        self._title = title
        if self.scholar_dict.keys().__contains__(scholar):
            self._scholar = scholar
        else:
            raise KeyError('Invalid Scholar Key.')
        self._soup = None
        self._result = None
        self._search_by_title()

    def _search_by_title(self):

        title = self._title

        if self._scholar == 'dblp':
            title = self._title.replace(' ', '$')

        url_title = parse.quote_plus(title)

        url = self.scholar_dict[self._scholar]['search'] + url_title

        try:
            text = requests.get(url, proxies=self.proxies, verify=False)
        except:
            raise ConnectionError

        if text.encoding != 'utf-8':
            text = text.text.encode(text.encoding).decode('utf-8')

        else:
            text = text.text

        self._soup = BeautifulSoup(text, 'html.parser')
        return True

    def _parse(self):
        tag_name = self.scholar_dict[self._scholar]['tag_name']
        class_name = self.scholar_dict[self._scholar]['class_name']

        result_tags = self._soup.find_all(tag_name, class_name)
        return self._find_exact_entry(result_tags)

    def _find_exact_entry(self, result_tags):
        found = False
        for tag in result_tags:
            title = tag.find(self.scholar_dict[self._scholar]['title_tag'],
                             self.scholar_dict[self._scholar]['title_class']
                             ).get_text().replace('.', '')
            if self._title.lower() == title.lower():
                found = True
                self.soup = tag
                break
        if not found:
            print('Title:%s not found.' % self._title)
        return found

    def get_bib(self):
        if self._parse():
            if self._scholar == 'dblp':
                bib_link = self.soup.find_all('li', 'drop-down')[1].find('a').get('href')

            elif self._scholar == 'bing':
                bib_link = 'https://academicapi.chinacloudsites.cn/Paper/Citation/%s?type=bibtex&encoded=0' % \
                           self.find('span', 'caption_cite').get('paperid')

            elif self._scholar == 'google':
                ref_link = 'https://scholar.google.com/scholar?q=info:%s:scholar.google.com/&output=cite&scirp=%s&hl=en' % \
                           (self.soup.get('data-cid'), self.soup.get('data-rp'))
                try:
                    ref_text = requests.get(ref_link, proxies=self.proxies, verify=False)
                    soup = BeautifulSoup(ref_text)
                    bib_link = soup.find('a', 'gs_citi').get('href')
                except:
                    raise ConnectionError

            try:
                text = requests.get(bib_link, proxies=self.proxies, verify=False)
                soup = BeautifulSoup(text.text, 'html.parser')
                text = soup.find(self.scholar_dict[self._scholar]['bib_text']).get_text()
            except:
                raise ConnectionError

            self._result = Record.Record()
            self._result.bibtex = text
            return self._result
        else:
            return None

=======
import requests
import urllib.parse as parse
from bs4 import BeautifulSoup
from . import Record

requests.packages.urllib3.disable_warnings()


# Get one reference information at a time
class Spider:
    ip_list = ['127.0.0.1:8087', '127.0.0.1:8086']
    user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                  'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                  'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                  'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    proxies = {'http': '127.0.0.1:8087',
               'https': '127.0.0.1:8087'}
    scholar_dict = {
        'google'    :{'search':'https://scholar.google.com/scholar?hl=en&q=',
                       'tag_name':'div',
                       'class_name':'gs_r gs_or gs_scl',
                       'title_tag':'h3',
                       'title_class':'',
                       'bib_text':'pre',
                      },
        'bing'      :{'search':'https://cn.bing.com/academic/search?q=',
                       'tag_name':'li',
                       'class_name':'aca_algo',
                       'title_tag': 'h2',
                       'title_class':'',
                       'bib_text':'pre',
                      },
        'dblp'      :{'search':'https://dblp.uni-trier.de/search?q=',
                       'tag_name':'li',
                       'class_name':'entry',
                       'title_tag': 'span',
                       'title_class':'title',
                       'bib_text':'pre',
                      },
    }

    def __init__(self, title, scholar):
        self._title = title
        if self.scholar_dict.keys().__contains__(scholar):
            self._scholar = scholar
        else:
            raise KeyError('Invalid Scholar Key.')
        self._soup = None
        self._result = None
        self._search_by_title()

    def _search_by_title(self):

        title = self._title

        if self._scholar == 'dblp':
            title = self._title.replace(' ', '$')

        url_title = parse.quote_plus(title)

        url = self.scholar_dict[self._scholar]['search'] + url_title

        try:
            text = requests.get(url, proxies=self.proxies, verify=False)
        except:
            raise ConnectionError

        if text.encoding != 'utf-8':
            text = text.text.encode(text.encoding).decode('utf-8')

        else:
            text = text.text

        self._soup = BeautifulSoup(text, 'html.parser')
        return True

    def _parse(self):
        tag_name = self.scholar_dict[self._scholar]['tag_name']
        class_name = self.scholar_dict[self._scholar]['class_name']

        result_tags = self._soup.find_all(tag_name, class_name)
        return self._find_exact_entry(result_tags)

    def _find_exact_entry(self, result_tags):
        found = False
        for tag in result_tags:
            title = tag.find(self.scholar_dict[self._scholar]['title_tag'],
                             self.scholar_dict[self._scholar]['title_class']
                             ).get_text().replace('.', '')
            if self._title.lower() == title.lower():
                found = True
                self.soup = tag
                break
        if not found:
            print('Title:%s not found.' % self._title)
        return found

    def get_bib(self):
        if self._parse():
            if self._scholar == 'dblp':
                bib_link = self.soup.find_all('li', 'drop-down')[1].find('a').get('href')

            elif self._scholar == 'bing':
                bib_link = 'https://academicapi.chinacloudsites.cn/Paper/Citation/%s?type=bibtex&encoded=0' % \
                           self.find('span', 'caption_cite').get('paperid')

            elif self._scholar == 'google':
                ref_link = 'https://scholar.google.com/scholar?q=info:%s:scholar.google.com/&output=cite&scirp=%s&hl=en' % \
                           (self.soup.get('data-cid'), self.soup.get('data-rp'))
                try:
                    ref_text = requests.get(ref_link, proxies=self.proxies, verify=False)
                    soup = BeautifulSoup(ref_text)
                    bib_link = soup.find('a', 'gs_citi').get('href')
                except:
                    raise ConnectionError

            try:
                text = requests.get(bib_link, proxies=self.proxies, verify=False)
                soup = BeautifulSoup(text.text, 'html.parser')
                text = soup.find(self.scholar_dict[self._scholar]['bib_text']).get_text()
            except:
                raise ConnectionError

            self._result = Record.Record()
            self._result.bibtex = text
            return self._result
        else:
            return None

>>>>>>> 46431f867d190d95d5b4df43f1fa349b9eb11098
