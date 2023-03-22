#!usr/bin/env python
#coding=utf-8


from Spider import Spider
from SpiderWeb1 import SpiderWeb1
from RWFile import RWFile
import argparse
import logging.config
import os

logging.config.fileConfig("./logging.conf")
logger = logging.getLogger(os.path.basename(__file__))

if __name__ == '__main__':
    # 用户参数处理
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Gave the max num to check.", type=int)
    args = parser.parse_args()

    source = args.source

    spider = Spider()
    if source == 1:
        # WEBb1
        spider = SpiderWeb1()
    proxy_list = spider.get_data()

    if len(proxy_list) > 0:
        logger.info(proxy_list)
        logger.info(len(proxy_list))
        if source > 0:
            RWFile.write_spider_file(proxy_list)
    else:
        logger.info("Got nothing.")










