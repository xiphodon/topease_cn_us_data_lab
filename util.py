#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 9:09
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : util.py
# @Software: PyCharm


import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import json
import numpy as np

show_my_print = True

def get_key_words(content):
    '''
    获取内容中关键字
    :param content:
    :return: 关键字拼接字符串（sep=","）
    '''
    # stemmer = SnowballStemmer('english')
    lemmatizer = WordNetLemmatizer()
    # 过滤标点符号
    maketran = str.maketrans(string.punctuation,' '*len(string.punctuation))
    content = str(content).translate(maketran)
    # 提取关键字(小写)
    word_list = word_tokenize(content.lower())
    # 分析关键字词性
    word_pos_tag_set = set(nltk.pos_tag(word_list))
    # print(word_pos_tag_set)
    # 筛选名词类关键词，筛选停止词，筛选关键词位数，筛选关键词是否含有数字，并提取词干/原型
    # word_pos_tag_NN_stem_set = {stemmer.stem(item[0]) for item in word_pos_tag_set if 'NN' in item[1] and len(item[0]) > 1 and not bool(re.search(r'\d', item[0]))}
    word_pos_tag_NN_stem_set = {lemmatizer.lemmatize(item[0])
                                for item in word_pos_tag_set
                                if
                                # 'NN' in item[1]
                                item[0] not in stopwords.words('english')
                                and len(lemmatizer.lemmatize(item[0])) > 1
                                and not bool(re.search(r'\d', item[0]))}
    # 关键字拼接
    word_pos_tag_NN_str = ",".join(word_pos_tag_NN_stem_set)

    # print(word_pos_tag_NN_str)

    return word_pos_tag_NN_stem_set


def filter_desc(product_desc_list):
    '''
    过滤产品描述信息
    :return: 过滤后的迭代类型（map）
    '''
    return map(lambda x:str(x).replace('<br/>', ''), product_desc_list)




def read_hs_mapping_json():
    with open(r'./data/HS_code_6.json','r',encoding='utf8') as fp:
        hs_mapping_str = fp.read()
        return json.loads(hs_mapping_str)


hs_mapping_dict = read_hs_mapping_json()


def check_hs_code_mapping_desc(hs_str):
    if hs_str == None:
        return ""
        # print("提示：请输入4~10位的HS编码")
    hs_str = str(hs_str).strip()
    if len(hs_str) < 4:
        return ""
        # print("提示：HS编码位数为4~10位")
    else:
        input_str_f4 = hs_str[:4]
        if input_str_f4 in hs_mapping_dict:
            hs_f4_dict = hs_mapping_dict[input_str_f4]
            f4_desc = hs_f4_dict['desc']
            if len(hs_str) >= 6:
                if 'next' in hs_f4_dict:
                    input_str_f4_6 = hs_str[4:6]
                    hs_f4_next_dict = hs_f4_dict['next']
                    if input_str_f4_6 in hs_f4_next_dict:
                        hs_f4_6_dict = hs_f4_next_dict[input_str_f4_6]
                        f4_6_desc = hs_f4_6_dict['desc']
                        return f4_desc + "," + f4_6_desc
                        # print("HS编码描述：", f4_desc + ',' + f4_6_desc)
                    else:
                        return f4_desc
                        # print("HS编码描述：", f4_desc)
                else:
                    return f4_desc
                    # print("HS编码描述：", f4_desc)
            else:
                return f4_desc
                # print("HS编码描述：", f4_desc)
        else:
            return ""
            # print("提示：未找到该HS编码匹配的类别，请检查输入的HS编码是否正确")


def hs2desc(hs_codes):
    '''
    hs转描述
    :param hs_codes:
    :return:
    '''

    if hs_codes == np.nan:
        hs_codes = ''

    # 一条订单有多个hs编码时
    hs_codes_list = str(hs_codes).split(',')
    # print(hs_codes_list)

    return ','.join(list(map(check_hs_code_mapping_desc, hs_codes_list)))


def filter_desc_and_get_desc_keys(hs2desc_list, product_desc_list):
    '''
    过滤产品描述信息&HS描述信息，并提取描述关键词
    :return:
    '''

    # hs2desc2keys_list = []
    # product_desc_keys_list = []
    # all_keys_list = []
    #
    # for hs2desc, product_desc in zip(hs2desc_list, product_desc_list):
    #
    #     this_item_hs2desc_keys_set = get_key_words(hs2desc)
    #     this_item_product_desc_keys_set = get_key_words(product_desc)
    #
    #     hs2desc2keys_list.append(','.join(this_item_hs2desc_keys_set))
    #     product_desc_keys_list.append(','.join(this_item_product_desc_keys_set))
    #
    #     all_keys_list.append(','.join(this_item_hs2desc_keys_set | this_item_product_desc_keys_set))

    my_print("filter desc and get desc keys (get keys set ...) ...")
    hs2desc2keys_set_list = [get_key_words(item) for item in hs2desc_list]
    my_print("filter desc and get desc keys (get keys set OK 1/3 ...) ...")
    product_desc_keys_set_list = [get_key_words(item) for item in product_desc_list]
    my_print("filter desc and get desc keys (get keys set OK 2/3 ...) ...")
    all_keys_set_list = [(item1 | item2) for item1,item2 in zip(hs2desc2keys_set_list,product_desc_keys_set_list)]
    my_print("filter desc and get desc keys (get keys set OK) ...")

    my_print("filter desc and get desc keys (get keys string ...) ...")
    hs2desc2keys_list = [','.join(item) for item in hs2desc2keys_set_list]
    my_print("filter desc and get desc keys (get keys string OK 1/3 ...) ...")
    product_desc_keys_list = [','.join(item) for item in product_desc_keys_set_list]
    my_print("filter desc and get desc keys (get keys string OK 2/3 ...) ...")
    all_keys_list = [','.join(item) for item in all_keys_set_list]
    my_print("filter desc and get desc keys (get keys string OK) ...")

    return hs2desc2keys_list, product_desc_keys_list, all_keys_list

def my_print(*args, sep=' ', end='\n', file=None):
    if show_my_print:
        print(*args, sep=' ', end='\n', file=None)

if __name__ == "__main__":
    print("\n===== HS查询系统 =====\n")
    while True:
        input_str = input("请输入HS编码（4~10位）：")
        if input_str == 'exit':
            print("\n===== 退出HS查询系统 =====\n")
            break
        else:
            print(check_hs_code_mapping_desc(input_str))

