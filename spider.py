"""T大树洞爬虫
"""
import json
import argparse
import os
import time
from tqdm import tqdm
from utils import getcomment, getlist
from utils import spider_one_page


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T大树洞爬虫, 程序会自动爬取帖子以及对应评论内容")
    # parser.add_argument("--start", help="爬取帖子索引最大值，若不指定，默认为最新帖子的id",
    #                     type=int)
    # parser.add_argument("--end", help=("爬取帖子索引最小值"
    #                                    "若不指定，程序会自动检测路径中索引最大的id"),
    #                     type=int)
    parser.add_argument("--config", help="爬虫配置文件路径",
                        default="./config.json")
    parser.add_argument("--store-path", help="数据存储目录",
                        default="./posts")
    parser.add_argument("--sleep", help="爬取一次页面后休眠时间/s", type=int, default=20)
    args = parser.parse_args()

    config_file = args.config
    #  加载参数
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
    sleep_time = args.sleep

    # 获取最新帖子pid
    max_pid = 0
    page = getlist(1, getlist_url)
    page = json.loads(page, encoding='utf-8')
    max_pid = max(map(lambda x: int(x['pid']), page['data']))

    # 确认爬取帖子索引最小值
    # if end is None:
    #     filenames = os.listdir(store_path)
    #     path_exist = os.path.exists(store_path)
    #     if path_exist and len(filenames) != 0:
    #         end = max(map(lambda x: int(x.split('.')[0]), filenames))
    #     elif not path_exist:
    #         os.makedirs(store_path)
    #         end = 0
    #     else:
    #         end = 0

    # 获取已爬取的帖子
    if os.path.exists(store_path):
        pid_list = map(lambda x: int(x.split('.')[0]),
                       os.listdir(store_path))
    else:
        os.makedirs(store_path)
        pid_list = []

    # 爬取页面
    p = 1
    page_num = max_pid // 30 + 1
    for p in tqdm(range(1, page_num + 1)):
        start_t = time.time()
        page = getlist(p, getlist_url)

        max_id, min_id = spider_one_page(page, getcomment_url,
                                        store_path, pid_list)
        # print((f"page: {p}, pid range: "
        #     f"({max_id}, {min_id})"
        #     f", cost time: {time.time() - start} s"))
        time.sleep(sleep_time)

    
        
        

