import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scraper import Scraper
import requests
import json
import shutil
import datetime

''' The purpose of this script is to crawl pictures from index json file generated from tieba_bot.py'''
# After scraping the title, link from certain tieba, we're now digging the contents.

# Version 1.0

# Load dict ionary
def load_json(filename):
    data = json.load(open(filename))
    return data

# Dump dictionary back
def dumpjson(dictionary, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(dictionary, f, ensure_ascii=False)

# Split dictionary into multiple blocks of orders:
def dictsplit():
    pass

# Controller of overall Crawling
def task_manager(data, filename):
    pre_url = "https://tieba.baidu.com"
    for key, value in data.items():
        if value["crawled"]:
            print('skipping %s due to crawled' % key)
            continue
        url = pre_url + key
        name = value["author"]
        title = value["title"]
        print("\n\nCrawling %s 的 %s" % (name, title))
        try:
            page_crawl(url, name)
            value["crawled"] = False
        except Exception as e:
            print("Crawl failed on %s" % name)
            print(e)
            break
    dumpjson(data, filename)

# Specific page search
def page_crawl(url, name):
    scraper = Scraper(selenium = True, sleeptime = 15)
    scraper.set_url(url)
    REQUEST_1 = [{'css_selector': '.wrap1 .l_container .left_section .d_post_content_main'}]
    REQUEST_2 = [{'css_selector': 'cc .d_post_content'}]
    REQUEST_3 = [{'css_selector': 'img.BDE_Image'}]
    scraper.set_soup_select(REQUEST_1, REQUEST_2, REQUEST_3)
    scraper.run()
    # print(scraper.nth_res[0][0])
    img_src = []
    for each in scraper.nth_res[2][0]:
        src = each.get("src")
        img_src.append(src)
        print("image acquired %s" % src)
    for each in img_src:
        crawl_images(name, each)

def crawl_images(name, src, folder = "../.Pictures/"):
    global records
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    try:
        if not os.path.exists(os.path.join(folder,name)):
            os.mkdir(os.path.join(folder,name))
        print('downloading %s' % src)
        response = requests.get(src, stream=True, headers=header)
        i = 0
        while os.path.exists('%s%s/%s%s.jpg' % (folder, name, name, i)):
            i += 1
        with open(os.path.join(folder, name, name+str(i)+".jpg"), 'wb') as out:
            shutil.copyfileobj(response.raw, out)
        if name in records:
            records[name] += 1
        else:
            records[name] = 0
    except Exception as e:
        print('could not load %s' % src)
        print(e)

def record_save(records):
    monthday = datetime.datetime.now().month + datetime.datetime.now().day
    with open('%s-%s.log' % monthday[0], monthday[1], 'w') as fin:
        for k, v in records.items():
            fin.write(str(k) + '\t' + str(v) + '\n')

if __name__ == '__main__':
    records = {}
    filename = sys.argv[1]
    data = load_json(filename)
    task_manager(data, filename)
    record_save(records)
