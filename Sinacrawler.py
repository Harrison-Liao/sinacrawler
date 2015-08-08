#!/usr/bin/python
# -*- coding:utf8 -*-
#by domon
#domon@live.cn
from lxml import etree
import csv
import time
import requests
import urllib2
from multiprocessing.dummy import Pool as ThreadPool #用pool.map 方式实现多线程正文提取
import sys
reload(sys)
sys.setdefaultencoding('utf8')
start = time.time() #计时器初始化
print start
def core(urleach): #正文提取函数，用Xpath 方式匹配内容
    url = urleach.xpath('//span[@class="atc_title"]/a/@href')#.extract()
    for i in range(len(url)):
        #print url[i]
        response = urllib2.urlopen(url[i])
        html = response.read().decode('utf-8')
        selector = etree.HTML(html)
        title = selector.xpath('//h2/text()')[0] #提取文章标题
        date = selector.xpath('//span[@class="time SG_txtc"]/text()')[0] #提取文章发表日期
        content = selector.xpath('//*[@id="sina_keyword_ad_area2"]/p/text()') #提取正文，即提取所有P表现内容为集合
        content2 = " ".join(content) #将正文合并为字符串
        writer = csv.writer(csvfile)
        csvfile.write('\xEF\xBB\xBF') #预先写入这个部分是为了防止CSV 中文乱码
        data = [date,title,content2] #写入内容，每篇文章一行三列
        writer.writerow(data)
    csvfile.close() #关闭文件
pageurl = 'http://blog.sina.com.cn/s/articlelist_1596566922_0_1.html' #新浪博客文章列表地址，由于文章列表地址是规律命名，翻页可以简单实现
print pageurl
csvfile = file('test.csv','a+') #CSV文件属性，追加方式写入
html = requests.get(pageurl) #如需对传递信息做特殊处理，可以修改这个部分
selector = etree.HTML(html.text)
content_field = selector.xpath('//*[@id="module_928"]/div[2]/div[1]/div[@class="articleList"]') #提取了文章列表中每篇文章对应地址

#多线程部分
worker = 4 #设置4个线程
pool = ThreadPool(worker)
results = pool.map(core, content_field) #以pool.map 方式实现多线程，替代的是单线程中的for循环
pool.close()
pool.join()
print "Threadpool = %s" % worker #打印线程数，方便调试
print "Elapsed time: %s" % (time.time()-start) #打印消耗的时间
