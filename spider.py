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
    parser.add_argument("--sleep-factor", help="爬取一个未曾读取的帖子后休眠时间/s",
                        type=int, default=1)
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
    sleep_factor = args.sleep_factor

    # 获取最新帖子pid
    max_pid = 0
    page = getlist(1, getlist_url)
    page = json.loads(page, encoding='utf-8')
    max_pid = max(map(lambda x: int(x['pid']), page['data']))

    # 获取已爬取的帖子
    if os.path.exists(store_path):
        pid_list = list(map(lambda x: int(x.split('.')[0]),
                            os.listdir(store_path)))
    else:
        os.makedirs(store_path)
        pid_list = []
    print(len(pid_list), max(pid_list))
    
    # 爬取页面
    p = 478
    page_num = max_pid // 30 + 1
    for p in tqdm(range(p, page_num + 1)):
        start_t = time.time()
        page = getlist(p, getlist_url)

        count = spider_one_page(page, getcomment_url,
                                        store_path, pid_list)
        time.sleep(1 + count * sleep_factor)

    
        
        

