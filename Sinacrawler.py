#!/usr/bin/python
# -*- coding:utf8 -*-
from lxml import etree
import csv
import time
import requests
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf8')
start = time.time()
print start
def core(urleach):
    url = urleach.xpath('//span[@class="atc_title"]/a/@href')#.extract()
    for i in range(len(url)):
        #print url[i]
        response = urllib2.urlopen(url[i])
        html = response.read().decode('utf-8')
        selector = etree.HTML(html)
        title = selector.xpath('//h2/text()')[0]
        date = selector.xpath('//span[@class="time SG_txtc"]/text()')[0]
        content = selector.xpath('//*[@id="sina_keyword_ad_area2"]/p/text()')
        content2 = " ".join(content)
        writer = csv.writer(csvfile)
        csvfile.write('\xEF\xBB\xBF')
        data = [date,title,content2]
        writer.writerow(data)
    csvfile.close()
pageurl = 'http://blog.sina.com.cn/s/articlelist_1596566922_0_1.html'
print pageurl
csvfile = file('test.csv','a+')
html = requests.get(pageurl)
selector = etree.HTML(html.text)
content_field = selector.xpath('//*[@id="module_928"]/div[2]/div[1]/div[@class="articleList"]')

# Make the Pool of workers
worker =
pool = ThreadPool(worker)
# Open the urls in their own threads
# and return the results
results = pool.map(core, content_field)
#close the pool and wait for the work to finish
pool.close()
pool.join()
print "Threadpool = %s" % worker
print "Elapsed time: %s" % (time.time()-start)