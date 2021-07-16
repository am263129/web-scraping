import csv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
import time, threading
import queue,sys,subprocess
import pickle
from threading import Thread


DRIVER_PATH = "./chromedriver"
INPUT = "keywords.csv"
OUTPUT = "products.csv"
Queue = queue.LifoQueue()
completeCount = 0

def Create_driver():

    # capabilities['proxy']['socksUsername'] = proxy['username']
    # capabilities['proxy']['socksPassword'] = proxy['password']
    prefs = {
        "translate_whitelists": {'ja': 'en'}, # translate from Japanese to English
        "translate": {'enabled': 'true'}
    }

    options = Options()
    # options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    # options.add_argument("--headless") # do not open browser
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    options.add_argument("--enable-automation")
    options.add_argument("--test-type=browser")
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path="./chromedriver", options = options)
    # desired_capabilities=capabilities  
    return driver


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
    driver = Create_driver()    
    while not Queue.empty():
        driver.get("https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + Queue.get())
        productlist = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[1]/h2/a')
        producturls = []
        for product in productlist:
            producturls.append(product.get_attribute('href'))
        for i in range(len(producturls)):
            url = producturls[i]
            # print("getting product :"+url)
            # check if url is valid
            if not ("https://" in url):
                continue
            driver.get(url)
            name = ""
            price = ""
            asin = ""

            #japanese
            # name = driver.find_element_by_xpath('//*[@id="productTitle"]/font/font').get_attribute("innerHTML")
            # price = driver.find_element_by_xpath('//*[@id="price_inside_buybox"]/font/font').get_attribute("innerHTML")
            # asin = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td/font/font').get_attribute("innerHTML")
            #english
            try:
                name = driver.find_element_by_xpath('//*[@id="productTitle"]').get_attribute("innerHTML")
                price = driver.find_element_by_xpath('//*[@id="price_inside_buybox"]').get_attribute("innerHTML")
                asin = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td').get_attribute("innerHTML")
            except:
                pass
            save_all_data(name,price,asin)
            global completeCount
            completeCount += 1
            print("%i Products are completed" % completeCount)

        Queue.task_done()
    driver.close()

if __name__ == '__main__':
    file = open(INPUT, encoding="utf8")
    keywords = file.readlines()
    numKeyword = 0

    for keyword in keywords:
        Queue.put(keyword)

    for i in range(5):
        print("Start one thread")
        t1 = Thread(target = do_scrap)
        numKeyword += 1
        print("scrap keyword %i",numKeyword)
        t1.start()
    Queue.join()
    print("Completed")
        


