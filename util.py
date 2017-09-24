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
    # 筛选名词类关键词，筛选关键词位数，筛选关键词是否含有数字，并提取词干/原型
    # word_pos_tag_NN_stem_set = {stemmer.stem(item[0]) for item in word_pos_tag_set if 'NN' in item[1] and len(item[0]) > 1 and not bool(re.search(r'\d', item[0]))}
    word_pos_tag_NN_stem_set = {lemmatizer.lemmatize(item[0])
                                for item in word_pos_tag_set
                                if 'NN' in item[1]
                                and len(lemmatizer.lemmatize(item[0])) > 1
                                and not bool(re.search(r'\d', item[0]))}
    # 关键字拼接
    word_pos_tag_NN_str = ",".join(word_pos_tag_NN_stem_set)

    return word_pos_tag_NN_str


def filter_desc(product_desc_list):
    '''
    过滤产品描述信息
    :return: 过滤后的迭代类型（map）
    '''
    return map(lambda x:str(x).replace('<br/>', ''), product_desc_list)

