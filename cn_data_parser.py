#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 9:08
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : cn_data_parser.py
# @Software: PyCharm


import pandas as pd
import os
import numpy as np
import util
import time
import datetime
import requests
import json
import urllib.parse

base_path = r"E:\work_all\topease\CN_data\database_sep_^\201604_201611"

debug = True


def read_cn_data():
    '''
    读取中国海关数据（2016.04 - 2016.11）
    :return:
    '''
    file_list = os.listdir(base_path)

    col_name = ['海关编码', '商品名称', '出口最终国或进口原产国', '中转国', '企业名称']
    data = pd.DataFrame(columns=col_name)

    for file_name in file_list:
        file_path = os.path.join(base_path, file_name)
        temp_data = pd.read_csv(file_path, encoding='ansi', sep='^', dtype=np.str)

        if debug:
            # 实验样本
            temp_data = temp_data.iloc[:10000, :]

        temp_data = temp_data[col_name]

        # data = pd.concat([data,temp_data],axis=0)
        data = data.append(temp_data)

        # print(file_path)
        util.my_print("len(data):", len(data))

        if debug:
            # 实验数据
            return data

    return data


google_translate_url = r'http://translate.google.cn/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q='
headers = {'Host': 'translate.google.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://translate.google.cn/',
           'Connection': 'keep-alive'}



def cn2en(cn_str):
    '''
    中译英
    :param cn_str:中文，需加密（密文形如：%E4%BB%8A%E5%A4%A9%E5%A4%A9%E6%B0%94%E4%B8%8D%E9%94%99）
    :return:
    '''
    encode_cn_str = urllib.parse.quote(cn_str)
    r = requests.get(google_translate_url + encode_cn_str, headers=headers)
    en_str = json.loads(r.text)[0][0][0]
    return en_str



if __name__ == '__main__':
    data = read_cn_data()
    data['hs2desc'] = [util.hs2desc(item) for item in data['海关编码']]
    data['cn_product_desc2en_product_desc'] = [cn2en(item) for item in data['商品名称']]
    data.to_csv(r'./temp_data/cn_10000.csv', sep='\t', index=False, encoding='utf8')
    print("finish")
