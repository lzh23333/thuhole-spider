"""T大树洞爬虫
"""
import json
import argparse
import os
import time
from utils import getcomment, getlist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T大树洞爬虫")
    parser.add_argument("--start", help="爬取帖子索引最大值，若不指定，默认为最新帖子的id",
                        type=int)
    parser.add_argument("--end", help=("爬取帖子索引最小值"
                                       "若不指定，程序会自动检测路径中索引最大的id"),
                        type=int)
    parser.add_argument("--config", help="爬虫配置文件路径",
                        default="./config.json")
    parser.add_argument("--store-path", help="数据存储目录",
                        default="./data")
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
    end = args.end
    store_path = args.store_path
    sleep_time = args.sleep

    max_pid = 0
    start = args.start
    page = getlist(1, getlist_url)
    page = json.loads(page, encoding='utf-8')
    max_pid = max(map(lambda x: int(x), page['data'].keys()))
    if start is None:
        start = max_pid

    # 确认爬取帖子索引最小值
    if end is None:
        filenames = os.listdir(store_path)
        path_exist = os.path.exists(store_path)
        if path_exist and len(filenames) != 0:
            end = max(map(lambda x: int(x.split('.')[0]), filenames))
        elif not path_exist:
            os.makedirs(store_path)
            end = 0
        else:
            end = 0

    # spider
    p = 1
    reach_end = False
    while not reach_end:

        start = time.time()
        page = getlist(p, getlist_url)

        page = json.loads(page, encoding='utf-8')
        page_data = page['data']
        for post in page_data:
            pid = post['pid']
            if pid > end:
                comment = getcomment(pid, getcomment_url)
                post['comment'] = json.loads(comment, encoding='utf-8')
                dst = os.path.join(store_path, f"{pid}.json")
                with open(dst, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(post, ensure_ascii=False))
            elif pid <= end and p == 1:
                pass
            else:
                reach_end = True
        p += 1
        print((f"page: {p}, pid range: "
               f"{max([int(x['pid']) for x in page_data])} "
               f"———— {min([int(x['pid']) for x in page_data])}"
               f" cost time: {time.time() - start} s"))
        time.sleep(sleep_time)

