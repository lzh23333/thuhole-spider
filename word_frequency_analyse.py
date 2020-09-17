#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:  word_frequency_analyse.py
@introduction:
@time:  2020/09/06 20:01:03
@author:  lzh
@version:  1.0
'''
import os
import json
import jieba


post_dir = './posts'
filename =os.path.join(post_dir, '58885.json')
with open(filename, 'r') as f:
    post = json.load(f)
post_text = post['text']
print(post_text)
word_list = jieba.cut(post_text)
print(word_list)

