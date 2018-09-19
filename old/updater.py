import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scraper import Scraper
import json
import re
import datetime

''' The purpose of this script is to crawl indexes from Baidu Tieba '''
# Specifically images, hahahaha

# This script should gather all information entrees on specific tieba url.
def tieba_index(url):

    def anotate_time(timestr):
        if '201' in timestr:
            return False
        if ':' in timestr:
            return 0
        times = timestr.split('-')
        present = datetime.datetime.now()
        ctime = datetime.datetime(present.year, int(times[0]), int(times[1]), 0, 0, 0)
        elapsed = present - ctime
        return elapsed.days

    scraper = Scraper(selenium = True, sleeptime = 15)
    scraper.set_url(url)
    REQUEST_1 = [{'css_selector': '.content .main .threadlist_bright'}]
    REQUEST_2 = [{'css_selector': '.j_thread_list'}]
    REQUEST_3 = [{'css_selector': 'a.j_th_tit '},
                {'css_selector': '.col2_left span'},
                {'css_selector': '.tb_icon_author .frs-author-name-wrap a'},
                {'css_selector': '.is_show_create_time'}]
    scraper.set_soup_select(REQUEST_1, REQUEST_2, REQUEST_3)
    scraper.run()
    links_list = scraper.nth_res[2][0]
    votes_list = scraper.nth_res[2][1]
    author_list = scraper.nth_res[2][2]
    create_date = scraper.nth_res[2][3]
    filedict = {}
    for i in range(len(links_list)):
        votes = votes_list[i].text
        votes = int(votes)
        if votes < 40:
            continue
        create_time = create_date[i].text
        elapsed = anotate_time(create_time)
        if elapsed == False:
            continue
        if elapsed > 40:
            continue
        try:
            title = links_list[i].get("title")
            author = author_list[i].text
            author = namestr(author)
            info = {"title":title, "votes": votes, "author": author, "crawled": False}
            filedict[links_list[i].get("href")] = info
            print(title, elapsed, votes)
        except Exception as e:
            print(e)
            break
    # print(filedict)
    # dumpjson(filedict, 'tieba_test.json')
    return filedict

def namestr(name):
    name = re.sub('[!@#$….]', '', name)
    return name

def dumpjson(dictionary, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(dictionary, f, ensure_ascii=False)

def create_dir():
    if not os.path.exists('repo'):
        os.mkdir('repo')

def crawl_all(bar_name, num_low, num_high, i):
    crawlist = range(num_low, num_high, 50)
    repo = {}
    for each in crawlist:
        tieba_url = "https://tieba.baidu.com/f?kw="
        tieba_url += bar_name
        tieba_url += '&pn=' + str(each)
        # print(tieba_url)
        files = tieba_index(url = tieba_url)
        repo.update(files)
    dumpjson(repo, os.path.join('../.repo', bar_name + '_repo%s.json' % i))

if __name__ == '__main__':
    bar_name = sys.argv[1]
    page_num = 1000
    if len(sys.argv) > 2:
        page_num = int(sys.argv[2])
    create_dir()
    crawl_all(bar_name, 0, page_num, 'update')
    # for i in range(repoid):
    #     crawl_all(bar_name, i*500, (i+1)*500, i)
