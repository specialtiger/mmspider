#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File        :图集谷.py
@Time        :2020/09/03 20:35:04
@Author      :hejiang
@Software    :vsCode
'''


from lxml import etree
import requests
import math
import os
import re
import random
import sys

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}
url = "https://www.tujigu.com/"
#设置重连次数
requests.adapters.DEFAULT_RETRIES = 5
# 设置连接活跃状态为False
s = requests.session()
s.keep_alive = False

def download_all():
    response = requests.get(url, headers=headers, timeout=5)
    html = etree.HTML(response.content.decode())
    lis = html.xpath("//li[@id='tag']//li/a/text()")
    lis1 = html.xpath("//li[@id='tag']//li/a/@href")

    links_dict = {}
    for i in range(0, len(lis)):
        links_dict[i] = lis[i]

    # print(links_dict)

    for k in links_dict.items():
        print(k, end='\n')

    while True:
        try:
            choose = int(input("请选择分类对应的数字(-1退出)>>>:"))
            if choose == -1:
                return
            choose_url = lis1[choose]
            print("选择", lis[choose])
            print("即将打开链接: %s" % choose_url)
            break
        except:
            print("请输入0-%d之间的数字。" % len(lis))

    resp = requests.get(choose_url, headers=headers, timeout=5)
    f = etree.HTML(resp.content.decode())
    count = f.xpath('//div[@class="shoulushuliang"]//span/text()')[0]
    pages = math.ceil(int(count)/40)
    print("此分类共包含%s套写真集,共计%s页。" % (count, pages))

    # 下载所有页面
    for i in range(1,pages+1):
        download_page(i)

def download_page(page):
    if page == 1:
        target_url = choose_url
    else:
        target_url = choose_url + "index_" + str(page-1) + ".html"
    response2 = requests.get(target_url, headers=headers, timeout=5)

    html = etree.HTML(response2.content.decode())

    biaoti_list = html.xpath('//div[@class="hezi"]//li/p[@class="biaoti"]/a/text()')
    mode_links = html.xpath('//div[@class="hezi"]//li/a/@href')

    print(biaoti_list)
    print(mode_links)
    username = os.getenv("USERNAME")
    savepath = "/mnt/k/tujigu/"+lis[choose]+'/'
    try:
        os.mkdir(savepath)
    except:
        pass

    for i in range(len(mode_links)):
        download_one_page(mode_links[i], savepath)

def download_group(target_url, savepath="/mnt/k/tujigu/精选/"):
    response = requests.get(target_url, headers=headers, timeout=5)
    html = etree.HTML(response.content.decode())

    biaoti_list = html.xpath('//div[@class="hezi"]//li/p[@class="biaoti"]/a/text()')
    mode_links = html.xpath('//div[@class="hezi"]//li/a/@href')

    biaoti = html.xpath('//title/text()')[0]
    biaoti = re.match('\w+', biaoti).group(0)
    print(biaoti)
    print(biaoti_list)
    print(mode_links)
    savepath = "/mnt/k/tujigu/"+biaoti.replace('/', '_')+'/'
    try:
        os.mkdir(savepath)
    except:
        pass

    for i in range(len(mode_links)):
        download_one_page(mode_links[i], savepath)

def download_one_page(page_url, savepath="/mnt/k/tujigu/精选/"):
    model_num = re.findall('\d{1,6}', page_url)[0]
    response3 = requests.get(page_url)
    html = etree.HTML(response3.content.decode())

    # 创建文件夹
    biaoti = html.xpath('//title/text()')[0]
    print(biaoti)
    subdir = savepath + biaoti.replace('/', '_')
    subdir = subdir.strip()
    if os.path.exists(subdir):
        print(subdir)
        return
    os.mkdir(subdir)

    pics_count = html.xpath('//p[contains(text(),"图片数量")]/text()')[0]
    print("模特的号码是：%s，%s" % (model_num, pics_count))
    pics = re.findall('\d{1,3}', pics_count)[0]
    # h = {
    #     'User-Agent': random.choice(USER_AGENTS)
    # }
    except_cnt = 0
    try:
        for j in range(1, int(pics)+1):
            pic_link = "https://lns.hywly.com/a/1/" + model_num + "/" + str(j) + ".jpg"
            print("开始爬取%s" % pic_link)
            with open(subdir + "/" + str(j) + ".jpg", "wb") as file:
                file.write(requests.get(pic_link).content)
            print("保存为图片%s" % (subdir + "\\" + str(j) + ".jpg"))
    except Exception as e:
        except_cnt = except_cnt + 1
        if except_cnt > 2:
            print(e)

# load k           
# sudo mkdir /mnt/k
# sudo mount -t drvfs K: /mnt/k

if __name__ == "__main__":
    # 'https://www.tujigu.com/a/8396/'
    if len(sys.argv) > 1:
        s = sys.argv[1]
        if s.find('\t\')!=-1:
            download_group(sys.argv[2])
        else:
            download_one_page(sys.argv[1])
    else:
        download_all()

