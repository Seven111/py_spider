#!usr/bin/env python
#coding=utf-8

import datetime
import os


class RWFile:

    @classmethod
    def write_spider_file(cls, proxy_list):
        if len(proxy_list) > 0:
            dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_file = '../proxy/spider-%s.txt' % dt_ms
            write_data = '\n'.join(proxy_list)
            RWFile.write(output_file, write_data)

    @classmethod
    def write_checked_file(cls, proxy_list):
        if len(proxy_list) > 0:
            dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_file = '../proxy/tested-%s.txt' % dt_ms
            write_data = '\n'.join(proxy_list)
            RWFile.write(output_file, write_data)

    # 将数据写入文件（txt）
    @classmethod
    def write(cls, output_file, data):
        path = os.path.split(output_file)[0]
        if not os.path.isdir(path):
            os.makedirs(path)
        print(output_file)
        with open(output_file, "w+") as f:
            f.write(data)


# if __name__ == '__main__':
#     RWFile.write_check_file(["1.1.1.1:0000:US:0001"])
