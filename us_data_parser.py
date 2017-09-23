#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 9:08
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : us_data_parser.py
# @Software: PyCharm

import pandas as pd
import os
import numpy as np
import util
import time
import datetime

base_path = r"E:\work_all\topease\US_data\database_sep_tab\dbo_usa_201607_09"

def read_us_data():
    '''
    读取美国海关数据（2016.07 - 2016.09）
    :return:
    '''
    file_list = os.listdir(base_path)

    col_name = ['HS Code', 'Actual Arrival Date', 'Consignee Name', 'Shipper Name', 'Product Desc', 'Country']
    data = pd.DataFrame(columns=col_name)

    for file_name in file_list:
        file_path = os.path.join(base_path,file_name)
        temp_data = pd.read_csv(file_path, encoding='ansi', sep='\t', dtype=np.str)

        # temp_data = temp_data.iloc[:1000,:]

        temp_data = temp_data[col_name]

        # data = pd.concat([data,temp_data],axis=0)
        data = data.append(temp_data)

        # print(file_path)
        print("len(data):",len(data))

        # return data

    return data


def filter_desc_and_get_desc_keys(product_desc_list):
    '''
    过滤描述信息，并提取描述关键词
    :return:
    '''
    return list(map(lambda x: util.get_key_words(str(x).replace('<br/>', '')),product_desc_list))



if __name__ == '__main__':

    print(datetime.datetime.now())
    time1 = time.time()

    print("start...")
    data = read_us_data()
    print("get data OK...")

    data['Country'] = list(map(lambda x: str(x).split(',')[-1].strip(), data['Country']))
    print("filter country OK...")

    product_desc_list = data['Product Desc']
    data['product_desc_keys'] = filter_desc_and_get_desc_keys(product_desc_list)
    print("filter desc and get desc keys OK...")
    # 存数据
    data.to_csv(r'./temp_data/us_desc_keys.csv', sep='\t', index=False)
    print("save new data OK...")
    print("finish~")

    print(datetime.datetime.now())
    time2 = time.time()
    print(time2 - time1)

    # print("find nike...")
    # print([item for item in data['product_desc_keys'] if 'nike' in item])