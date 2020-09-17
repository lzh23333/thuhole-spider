#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:  spilt_post_comment.py
@introduction:
@time:  2020/09/15 22:27:43
@author:  lzh
@version:  1.0
'''

import json
import os
from tqdm import tqdm


folder = './posts'
comment_folder = './comments'
for filename in tqdm(os.listdir(folder)):
    post_file = os.path.join(folder, filename)
    comment_file = os.path.join(comment_folder, filename)
    with open(post_file, 'r', encoding='utf-8') as f:
        try:
            post = json.load(f)
        except:
            print(post_file)
    if 'comment' not in post:
        continue
    else:
        print(post_file)
        continue
    comments = post['comment']
    post.pop('comment')
    with open(post_file, 'w') as f:
        f.write(json.dumps(post))
    with open(comment_file, 'w') as f:
        f.write(json.dumps(comment_file))
