#!usr/bin/env python
#coding=utf-8

""""
##  从网址【https://freeproxyupdate.com/socks5-proxy】  爬取IP:Port。
##  1、支持多线程翻页爬取。
##  2、支持HTML/Json解析  (BeautifulSoup, json) 需要自己实现
##  3、支持过滤：按国家、端口、延时过滤
##  4、返回符合筛选条件的数据
## 返回:html like
 <div class="">
     <table class="table">
         <thead>
             <tr>
                 <th>IP</th>
                 <th>Port</th>
                 <th>Country</th>
                 <th>State</th>
                 <th>City</th>
                 <th>Isp</th>
                 <th>Ping</th>
                 <th>Uptime</th>
                 <th>Type</th>
                 <th>Usage type</th>
                 <th>Spamhaus</th>
                 <th>Last updated</th>

             </tr>

         </thead>
         <tbody>
             <tr>
                 <td>174.64.199.79</td>
                 <td>4145</td>
                 <td>United States</td>
                 <td>Louisiana</td>
                 <td>Baton Rouge</td>
                 <td class="cut-text">Cox Communications Inc.</td>
                 <td>
                     <div class="d-flex">
                         <div class="mark-yellow"></div>
                         <div>179ms</div>

                     </div>

                 </td>
                 <td>98%</td>
                 <td>socks5</td>
                 <td>Residential (ISP)</td>
                 <td>
                     <a target="_blank" href="https://check.spamhaus.org/not_listed/?searchterm=174.64.199.79" class="text-success">not listed</a>

                 </td>
                 <td>34 seconds ago</td>

             </tr>
         </tbody>
     </table>
 </div>
"""

import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup  ## 用于HTML解析
from Spider import *


BASE_URL = 'https://freeproxyupdate.com/socks5-proxy'
PAGE_SIZE = 1
SPIDER_POOL_SIZE = 8
SPIDER_NET_TIME_OUT = 6*60


# 过滤
BASE_COUNTRY_SWITCH_WHITE = False  # True
BASE_COUNTRY_SWITCH_BLACK = (not BASE_COUNTRY_SWITCH_WHITE)

BASE_COUNTRY_WHITE = ',US,IN,DE,'    # Black list
BASE_COUNTRY_BLACK = ',CN,HK,IR,RU,'  # White list

BASE_PORT_BLACK = ',80,8080,4145,9050,7497,'  # Black list

# proxy延时限制
BASE_PROXY_SPEED_DELAY_LIMIT = 8000


class SpiderWeb1(Spider):

    @staticmethod
    def __filter(ip, port, country, ut):
        if len(ip) <= 0 or len(port) <= 0 or len(country) <= 0:
            return False
        # # 国家白名单处理
        if BASE_COUNTRY_SWITCH_WHITE and BASE_COUNTRY_WHITE.find(',' + country + ',') < 0:
            return False
        # # 国家黑名单处理
        if BASE_COUNTRY_SWITCH_BLACK and BASE_COUNTRY_BLACK.find(',' + country + ',') >= 0:
            return False
        # # port 位数限制 5位
        # if len(port) < 5: continue
        if BASE_PORT_BLACK.find(',' + port + ',') >= 0:
            return False
        #更新时间
        if ut > BASE_PROXY_SPEED_DELAY_LIMIT:
            return False
        return True

    @staticmethod
    def __change_country(country):
        country_map = {
            "United States": "US",
            "United Kingdom": "GB",  # 英国
            "Finland": "FI",  # 芬兰
            "Spain": "ES",  # 西班牙
            "Netherlands": "NL",  # 新西兰
            "Poland": "PL",  # 波兰
            "France": "FR",  # 法国
            "Germany": "DE",  # 德国
            "India": "IN",  # 印度
            "Turkey": "TR",  # 土耳其
            "Singapore": "SG",  # 新加坡
            "Canada": "CA",  # 加拿大
            "South Korea": "KR",  # 韩国
            "Japan": "JP",  # 日本
            "Vietnam": "VN",  # 越南
            "Italy": "IT",  # 意大利
            "MD": "MD",  # 缅甸
            "Iceland": "IS",  # 冰岛
            "Switzerland": "CH",  # 瑞士
            "Indonesia": "ID",  # 印尼
            "Luxembourg": "LU",  # 卢森堡
            "Brazil": "BR",  # 巴西
            "Bangladesh": "BD",  # 孟加拉
            "Colombia": "CO",  # 哥伦比亚
            "Venezuela": "VE",  # 委内瑞拉
            "1": "1"
        }
        if country_map.__contains__(country.strip()):
            return country_map[country]
        return ""

    def __parse_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        trs = tbody.find_all_next('tr')
        proxylist = []
        i = -1
        for tr in trs:
            i += 1
            if len(tr) <= 10: continue

            td = tr.find_all_next('td')
            if len(td) <= 2: continue

            ip = td[0].contents[0].strip()
            port = td[1].contents[0].strip()
            country = td[2].findNext().get_text().strip()
            country = SpiderWeb1.__change_country(country)
            if len(country) < 0: continue

            ut = 0
            if SpiderWeb1.__filter(ip, port, country, ut):
                proxylist.append('%s:%s:%s:%s' % (ip, port, country, ut))
        return proxylist

    def get_html(self, index):
        ret = (-1, index, [])
        url = BASE_URL  # 爬取单页
        # url = BASE_URL % index  # 支持翻页
        print(url)
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('Connection', 'keep-alive')]
            opener.addheaders = [('Cache-Control', 'no-cache')]
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)')]
            opener.addheaders = [('Accept', '*/*')]
            opener.addheaders = [('accept-encoding', 'gzip, deflate')]
            opener.addheaders = [('accept-language', 'zh-CN')]
            response = opener.open(url, timeout=SPIDER_NET_TIME_OUT)
        except urllib.error.HTTPError as e:
            print("[error_url:] " + url)
            print("[" + e.code + "]" + e.read().decode("utf8"))
        else:
            html = response.read()
            # print(html)
            ret = (0, index, self.__parse_data(html))
        finally:
            opener.close()
            time.sleep(1)
            return ret
        return ret

    def get_data(self):
        urls = [x for x in range(1, PAGE_SIZE + 1)]  # 并不是真的url
        proxy_list = []
        # 1、 线程池 爬取 ip  =>proxy_list
        with ThreadPoolExecutor(min(SPIDER_POOL_SIZE, PAGE_SIZE)) as executor:
            for data in executor.map(self.get_html, urls):
                print("ret:%d index:%d ret_num:%d" % (data[0], data[1], len(data[2])))
                if len(data[2]) > 0 and data[0] == 0:
                    proxy_list.extend(data[2])
            proxy_list = list(set(proxy_list))  # 去重
        return proxy_list


# if __name__ == '__main__':
#
#     spider = SpiderWeb1()
#     proxy_list = spider.get_data()
#     print(len(proxy_list))
#     print(proxy_list)


