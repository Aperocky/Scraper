from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# A SIMPLE SPIDER FOR QUICK SCRAPING
''' This scraper uses selenium and beautifulsoup to crawl informations in a
top - down controlled manner, scripts can also be injected '''

# Version 1.0, selection based on specific tags

# VERSION 1.1: Integrated css selector

# VERSION 1.2:
# html tags are now deprecated.
# The entire Scraper should run on css.

class Scraper:

    # Set header to User-Agent value.
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    def __init__(self, selenium = False, css= True, sleeptime = 10):
        self.url = ''
        self.soup_select = {}
        self.soup = ''
        self.nth_res = {}
        self.results = []
        self.selenium = selenium
        self.css = css
        self.sleeptime = sleeptime

    def clear_results(self):
        self.nth_res = {}
        self.results = []

    def set_url(self, url):
        if not 'http' in url:
            url = 'http://' + url
        self.url = url

    def set_soup_select(self, *args):
        selector = self.soup_select
        for i in range(len(args)):
            selector[i] = args[i]
        self.soup_select = selector

    def crawl(self):
        if self.selenium:
            special_spider = Selenium()
            special_spider.driver.get(self.url)
            sleep(self.sleeptime)
            html = special_spider.driver.page_source
            special_spider.quit()
        else:
            html = requests.get(self.url, headers=self.header).content
        soup = BeautifulSoup(html, 'lxml')
        self.soup = soup
        # print(html)
        # print(self.soup.prettify())

    def nth_extract(self, n):

        # GET SOUP AND SELECTOR for the particular iteration
        soup = self.soup
        select = self.soup_select[n]
        self.nth_res[n] = []

        # EXTRACT EACH REQUEST OF THE ITERATION
        for i in range(len(select)):
            selector = select[i]

            # Create an independent dictionary selector - such that modifying it will not affect the original selector
            class_selector = dict(selector)

            # Set Path
            path = 0
            if 'path' in selector:
                path = selector['path']
                del class_selector['path']

            # deprecated, SHOULD USE CSS!
            if not self.css:
                # Set tag
                tag = ''
                if 'tag' in selector:
                    tag = selector['tag']
                    del class_selector['tag']

                # Set attribute
                if 'attr' in selector:
                    attr = selector['attr']
                    del class_selector['attr']

                # Set recursive
                recv = True
                if 'recursive' in selector:
                    recv = False
                    del class_selector['recursive']

            # Set selection method
            # select_css = False
            # css_selector = ''
            # if 'css' in selector:
            #     select_css = True
            css_selector = selector['css_selector']

            # Select based on selector
            if self.css:
                if n == 0:
                    a = soup.select(css_selector)
                else:
                    a = []
                    for b in self.nth_res[n-1][path]:
                        a.extend(b.select(css_selector))
            else:
                if n == 0:
                    a = soup.find_all(tag, class_selector, recursive=recv)
                else:
                    a = []
                    for b in self.nth_res[n-1][path]:
                        a.extend(b.find_all(tag, class_selector, recursive=recv))

            # Put result into layered storage.
            self.nth_res[n].append(a)

            # Get final result.
            ''' DEPRECATED, use nth_res instead '''
            if 'attr' in selector:
                result = []
                for each in a:
                    try:
                        if attr == 'all':
                            result.append(each)
                        else:
                            result.append(getattr(each, attr))
                            result.append(each[attr])
                    except Exception:
                        pass
                    result = list(filter(None.__ne__, result))
                self.results.append(result)

    def specific_extract(self):
        pass

    def run(self):
        print("Crawling %s" % self.url)
        self.crawl()
        leng = len(self.soup_select)
        print("Processing soup...\n\n")
        for i in range(leng):
            self.nth_extract(i)

class Selenium:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capa)
        self.driver.set_window_size(1440,900)
        # self.wait = WebDriverWait(self.driver, 20)

    def quit(self):
        self.driver.quit()

# Less overhead, just make it work!
class Basic_Scraper:

    # Set default header as client. I doubt if wikipedia cares but best practice
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    def __init__(self, url):
        self.url = url

    # Crawl content. convert it to bs4
    def crawl(self):
        html = requests.get(self.url, headers=self.header).content
        soup = BeautifulSoup(html, 'lxml')
        self.soup = soup

    # Search for desired content
    def search(self, css):
        results = self.soup.select(css)
        self.result = results

# Following are tests, it should work correctly crawling reddit titles from worldnews
if __name__=='__main__':
    Ely = Scraper()
    Ely.set_url('https://old.reddit.com/r/worldnews')
    REQUEST_1 = [{'css_selector': 'div.thing'}]
    REQUEST_2 = [{'css_selector': 'a.title'},
                {'css_selector': 'div.likes'}]
    Ely.set_soup_select(REQUEST_1, REQUEST_2)
    Ely.run()
    for result in zip(Ely.nth_res[1][0], Ely.nth_res[1][1]):
        print("%s \n SCORE: %s" % (result[0].text, result[1].text))
