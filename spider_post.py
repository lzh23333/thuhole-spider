#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:  spider_post.py
@introduction: T大树洞爬虫，爬取帖子部分
@time:  2020/09/17 23:41:02
@author:  lzh
@version:  1.0
'''


import json
import argparse
import os
import time
from tqdm import tqdm
from utils import getcomment, getlist
from utils import spider_one_page


def parse_args():
    parser = argparse.ArgumentParser(description="T大树洞爬虫, 程序会自动爬取帖子内容")
    parser.add_argument("--start", help="爬取帖子索引最大值，若不指定，默认为最新帖子的id",
                        type=int)
    parser.add_argument("--end",
                        help="爬取帖子索引最小值，若不指定，程序会自动检测路径中索引最大的id",
                        type=int)
    parser.add_argument("--config", help="爬虫配置文件路径",
                        default="./config.json")
    parser.add_argument("--store-path", help="数据存储目录",
                        default="./posts")
    parser.add_argument("--sleep-factor", help="爬取一个未曾读取的帖子后休眠时间/s",
                        type=float, default=0.1)
    parser.add_argument("--mode",
                        help=("爬取模式, normal对应根据start-end确定爬取范围,"
                              "fix-missing对应根据目录，补全缺失帖子"),
                        default="normal")
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
    max_pid = max(map(lambda x: int(x['pid']), page['data']))
    start_pid = max_pid if args.start is None else args.start
    end_pid = args.end if args.end is not None else 1

    # 获取已爬取的帖子
    if os.path.exists(store_path):
        pid_list = list(map(lambda x: int(x.split('.')[0]),
                            os.listdir(store_path)))
        if end_pid == 1:
            end_pid = max(pid_list)
    else:
        os.makedirs(store_path)
        pid_list = []
    
    # 根据start end 爬取页面
    if args.mode == "normal":
        start_page = (max_pid - start_pid) // 30 + 1
        end_page = (max_pid - end_pid) // 30 + 1
        print("spider mode: normal")
        print(f"spider pid range: {start_pid, end_pid}")
        print(f"spider page from {start_page} to {end_page}")
        for p in tqdm(range(start_page, end_page)):
            p_list = spider_one_page(p, getlist_url, store_path)
            time.sleep(1 + len(p_list) * sleep_factor)

    # 完整爬取，并忽略已爬取的帖子
    elif args.mode == 'fix-missing':
        page_num = max_pid // 30 + 1
        for p in tqdm(range(p, page_num + 1)):
            start_t = time.time()
            page = getlist(p, getlist_url)
            p_list = spider_one_page(page, getcomment_url,
                                    store_path, pid_list)
            time.sleep(1 + len(p_list) * sleep_factor)

    else:
        raise Exception(f"mode {args.mode} isn't supported")
        
        

