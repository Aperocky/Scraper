from bs4 import BeautifulSoup
import os
import requests
import time
import json
import time
import pandas as pd
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

""" 
CORE CLASS DEALING WITH OUTGOING REQUEST AND WEB CONTENT.
"""

class Scraper():

    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    def __init__(self, config):
        self.config_path = config
        self._parse_config()

    # Read Config from Json File
    def _parse_config(self):
        config = json.load(open(self.config_path))
        # print(config)
        self.selenium = config.get("selenium")
        self.urls = config.get("url")
        # NESTED CONFIG SOLUTION FOR COMPLEX SCRAPING.
        self.nest = config.get("css_nested")
        # OFFERS SELENIUM AND JAVASCRIPT SUPPORT FOR INTERACTION.
        if self.selenium:
            self.jsaction = config.get("jsaction")
            self.sleeptime = config.get("sleep_time")
            if len(self.urls) != self.sleeptime:
                raise ValueError("Each entree of URL need to have corresponding sleep for selenium")
            self._selenium()
        # OFFERS A COMPLIMENTARY PARSER FOR DICTIONARY.
        if "parse" in config:
            self.parse = True
            self.parser_config = config.get("parse")
            self.table_names = config.get("table_names")
            self.save = config.get("save")
            self.savedir = config.get("savedir")
            self.datadir = config.get("datadir")
            self.datestr = config.get("datestr")
        else:
            self.parse = False

    def _crawl(self, url, sleeptime = 5):
        if self.selenium:
            self.driver.get(url)
            time.sleep(sleeptime)
            for each in self.jsaction:
                self.driver.execute_script(each)
            html = self.driver.page_source
        else:
            html = requests.get(url, headers=Scraper.header).content
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def _identify(self, soup, selector, selector_rule):
        # Result is a dictionary
        res_1 = soup.select(selector)
        res_2 = []
        for each in res_1:
            if selector_rule == "text":
                res_2.append(each.text)
            else:
                res_2.append(each[selector_rule])
        return res_2

    def _controller(self):
        master = {}
        for url, site in self.urls.items():
            if site not in master:
                master[site] = {}
            print("Crawling {}".format(url))
            soup = self._crawl(url)
            self._nested(soup, master[site])
        return master

    def _nested(self, soup, book):
        for k, v in self.nest.items():
            self._nested_proc(k, v, soup, book)

    # Each nest have 3 attributes, name, child, rule
    def _nested_proc(self, key, val, soup, book):
        selector = key
        name = val["name"]
        rule = val["rule"]
        child = val["child"]
        multi = val.get("multi")
        subname = val.get("subname")
        if name not in book:
            if len(child) > 0:
                book[name] = {}
                if rule != "none" and subname is not None:
                    book[name][subname] = []
            else:
                book[name] = []
        # Get Master level soup
        soups = soup.select(selector)
        # Check for empty, if empty, always return.
        if len(soups) == 0:
            if len(child) == 0:
                book[name].append("")
            else:
                if rule != "none" and subname is not None:
                    book[name][subname].append("")
            return
        # Recursion starts here
        if len(child) > 0:
            for each in soups:
                if rule != "none" and subname is not None:
                    text = self._get_rule(each, rule)
                    book[name][subname].append(text)
                for k, v in child.items():
                    self._nested_proc(k, v, each, book[name])
        else:
            if multi is None:
                text = self._get_rule(soups[0], rule)
                book[name].append(text)
            else:
                for each in soups:
                    text = self._get_rule(each, rule)
                    book[name].append(text)

    def _get_rule(self, soup, rule):
        if rule == "text":
            return soup.text
        else:
            return soup[rule]

    def _parse_result(self, master):
        parser = self.parser_config
        master_table = []
        print("Parsing Master Dictionary.. ")
        for each in parser:
            dummy = each.copy()
            dammy = master.copy()
            while True:
                if type(dummy) is dict:
                    key = list(dummy.keys())[0]
                    dummy = dummy[key]
                    dammy = dammy[key]
                    continue
                else:
                    totlist = [dammy[e] for e in dummy]
                    totlist = list(map(list, zip(*totlist)))
                    subtable = pd.DataFrame(totlist, columns = dummy)
                    master_table.append(subtable)
                    break
        return master_table

    def run(self):
        master = self._controller()
        # print(master)
        if self.parse:
            master = self._parse_result(master)
            if self.save:
                if self.datadir is None:
                    raise ValueError("No data path specified")
                if self.savedir is None:
                    raise ValueError("No save folder name specified")
                if self.datestr is None:
                    self.datestr = ""
                datestr = datetime.strftime(datetime.now(), self.datestr)
                dirname = "{}_{}".format(self.savedir, datestr)
                try:
                    os.makedirs(os.path.join(self.datadir, dirname))
                except FileExistsError:
                    pass
                for i in range(len(master)):
                    master[i].to_csv(os.path.join(self.datadir, dirname, self.table_names[i]+".csv"), index=False, encoding='utf-8')
        else:
            if __name__ == "__main__":
                print("Crawl Finished, nothing to do. Dumping dictionary to your screen\n")
                time.sleep(1)
                print(master)
        if self.selenium:
            self.driver.quit()
        return master

    def _selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capa)
        self.driver.set_window_size(1440,900)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pass in the path to the config json file.")
    parser.add_argument('-c', '--config', action='store', help="Get Config path")
    args = parser.parse_args()
    print(args.config)
    sk = Scraper(args.config)
    sk.run()