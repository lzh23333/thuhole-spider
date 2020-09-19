#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:  spider_comment.py
@introduction: T大树洞爬虫，爬取评论部分
@time:  2020/09/17 23:41:32
@author:  lzh
@version:  1.0
'''


import json
import argparse
import os
import time
from tqdm import tqdm
from utils import getcomment, getlist
from utils import spider_comments


def parse_args():
    parser = argparse.ArgumentParser(description="T大树洞爬虫, 程序会自动爬取帖子评论")
    parser.add_argument("--start", help="爬取帖子索引最大值，若不指定，默认为最新帖子的id",
                        type=int)
    parser.add_argument("--end",
                        help="爬取帖子索引最小值，若不指定，程序会自动检测路径中索引最大的id",
                        type=int)
    parser.add_argument("--config", help="爬虫配置文件路径",
                        default="./config.json")
    parser.add_argument("--store-path", help="数据存储目录",
                        default="./comments")
    parser.add_argument("--sleep-factor", help="爬取一个未曾读取的帖子后休眠时间/s",
                        type=float, default=0.1)
    parser.add_argument("--n", help="每次爬取的评论数量(<=30)",
                        type=int, default=30)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # 加载参数
    config_file = args.config
    
    with open(config_file, 'r') as f:
        config = json.load(f)

    # API
    getone_url = (f"{config['api_url']}&action=getone&"
                f"user_token={config['user_token']}")
    getcomment_url = (f"{config['api_url']}&action=getcomment"
                    f"&user_token={config['user_token']}")
    getlist_url = (f"{config['api_url']}&action=getlist"
                f"&user_token={config['user_token']}")
    store_path = args.store_path
    sleep_factor = args.sleep_factor

    # 获取最新帖子pid
    max_pid = 0
    page = getlist(1, getlist_url)
    page = json.loads(page, encoding='utf-8')
    print(page)
    max_pid = max(map(lambda x: int(x['pid']), page['data']))
    start_pid = max_pid if args.start is None else args.start
    end_pid = args.end if args.end is not None else 1
    n = args.n
    assert n > 0, "n 应为正整数"

    # 根据start end 爬取页面
    print(f"spider pid range: {start_pid, end_pid}")
    s = end_pid
    print(s)
    with tqdm(total=start_pid - end_pid + 1) as pbar:
        while True:
            spider_comments(range(s, s + n), getcomment_url, store_path)
            time.sleep(n * sleep_factor)
            s += n
            
            if s > start_pid:
                pbar.update(s - start_pid)
                break
            else:
                pbar.update(n)
            
