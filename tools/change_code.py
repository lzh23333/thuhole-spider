#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:  change_code.py
@introduction: 针对json编码导致文件中中文只显示unicode编码问题进行修复
@time:  2020/09/17 23:43:05
@author:  lzh
@version:  1.0
'''

import os
import json
from tqdm import tqdm


def change(folder):
    for filename in tqdm(os.listdir(folder)):
        filename = os.path.join(folder, filename)
        data = None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError as e:
            print(e)
            with open(filename, 'r') as f:
                data = json.load(f)
        if data is None:
            print(f'invalid encode: {filename}')
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False))

change('./posts')
