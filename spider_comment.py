import json
import redis
import argparse
from tqdm import tqdm
import time
from utils import getcomment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T大树洞评论爬虫")
    parser.add_argument("start", help="从第start个帖子处开始爬取评论",
                        type=int)
    parser.add_argument("end", help="爬取评论终点", type=int)
    parser.add_argument("--config", help="爬虫配置文件路径",
                        default="./robot.json")
    parser.add_argument("--n", help="连续获取n次评论后暂停", type=int,
                        default=10)
    parser.add_argument("--sleep", help="休眠时间/s", type=int, default=20)
    args = parser.parse_args()


    with open(args.config, 'r') as f:
        config = json.load(f)

    getcomment_url = f"{config['api_url']}&action=getcomment&user_token={config['user_token']}"
    r = redis.StrictRedis(db=7)
    every_n_comments = args.n
    sleep_s = args.sleep

    # 爬取数据
    data = {}
    for i in tqdm(range(args.start, args.end)):
        try:
            c = getcomment(i, getcomment_url)
            data[i] = c
            if len(data) == every_n_comments:
                r.mset(data)
                data = {}
                time.sleep(sleep_s)
        except Exception as e:
            print(e)

    if len(data) != 0:
        r.mset(data)
    
        
        
    


    # c = getcomment(1, getcomment_url)

