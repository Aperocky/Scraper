from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from core import Scraper

class SeleniumScraper(Scraper):

    def _parse_config(self):
        super()._parse_config()
        self.sleeptime = self.config.get("sleep_time", 5)
        self.jsaction = self.config.get("jsaction", [])
        self.selenium_driver = self.get_selenium_driver()

    def get_selenium_driver(self):
        options = webdriver.FirefoxOptions()
        options.set_headless(True)
        capa = DesiredCapabilities.FIREFOX
        capa["pageLoadStrategy"] = "normal"
        driver = webdriver.Firefox(options=options, desired_capabilities=capa)
        return driver

    def _crawl(self, url):
        driver = self.selenium_driver
        driver.get(url)
        WebDriverWait(driver, self.sleeptime)
        for each in self.jsaction:
            driver.execute_script(each)
            WebDriverWait(driver, self.sleeptime)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup

if __name__ == '__main__':
    sk = SeleniumScraper('configs/reddit.json')
    df = sk.run()
    print(df)
