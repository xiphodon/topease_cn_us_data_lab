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
        file_path = os.path.join(base_path,file_name)
        temp_data = pd.read_csv(file_path, encoding='ansi', sep='^', dtype=np.str)

        if debug:
            # 实验样本
            temp_data = temp_data.iloc[:1000,:]

        temp_data = temp_data[col_name]

        # data = pd.concat([data,temp_data],axis=0)
        data = data.append(temp_data)

        # print(file_path)
        util.my_print("len(data):",len(data))

        if debug:
            # 实验数据
            return data

    return data



if __name__ == '__main__':
    data = read_cn_data()
    print(data.head())
