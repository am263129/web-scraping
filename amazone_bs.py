import csv
import requests
import os
import time, threading
import queue,sys,subprocess
from threading import Thread
from bs4 import BeautifulSoup
from lxml import etree


DRIVER_PATH = "./chromedriver"
INPUT = "keywords.csv"
OUTPUT = "products.csv"
Queue = queue.LifoQueue()
completeCount = 0



def save_all_data(productname = "", price = "", asin = "",):
    write_header = False
    if not os.path.exists('products.csv'):
        write_header = True
    with open('products.csv', 'a', newline='',encoding="utf-8") as csvfile:

        fieldnames = ['name','price', 'asin']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({'name' : productname,'price': price, 'asin': asin})


def do_scrap():
    if Queue.empty():
        print("Empty Queue")
        return
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/45.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})       
    while not Queue.empty():
        URL = "https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + Queue.get()
        print(URL)
        page = requests.get(URL, headers=HEADERS)
        
        soup = BeautifulSoup(page.content, "html.parser")
        dom = etree.HTML(str(soup))
        products = dom.xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[1]/h2/a')
        print(len(products))
        for product in products:
            SUBURL = 'https://www.amazon.co.jp/' + product.attrib['href']
            print(SUBURL)
            detailPage = requests.get(SUBURL, headers=HEADERS)
            detailsoup = BeautifulSoup(detailPage.content, "html.parser")
            detaildom = etree.HTML(str(detailsoup))

            name = ""
            price = ""
            asin = ""
            try:
                f = open("result.html", "w",encoding="utf-8")
                f.write(str(detailsoup))
                f.close()
                name = detaildom.xpath('//*[@id="productTitle"]')[0].text
                print(name)
                price = detaildom.xpath('//*[@id="price_inside_buybox"]')[0].text
                print(price)
                # asin = detaildom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td')[0].text
                # table_info = detailsoup.find(id="productDetails_detailBullets_sections1").find("tr")
                asin = detailsoup.select_one("#productDetails_db_sections tr > td").get_text(strip=True)
                # asin = table_info.find('td').get_text(strip=True)
                print(asin)
            except:
                pass    
            save_all_data(name,price,asin)
            global completeCount
            completeCount += 1
            print("%i Products are completed" % completeCount)
        Queue.task_done()

if __name__ == '__main__':
    file = open(INPUT, encoding="utf8")
    keywords = file.readlines()
    numKeyword = 0
    for keyword in keywords:
        Queue.put(keyword)
        print("put"+keyword)
    for i in range(3):
        print("Start one thread")
        t1 = Thread(target = do_scrap)
        numKeyword += 1
        print("scrap keyword %i",numKeyword)
        t1.start()
    Queue.join()
    print("Completed")
        


