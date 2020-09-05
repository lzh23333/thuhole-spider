import requests
import json
import os


HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   " AppleWebKit/537.36 (KHTML, like Gecko)"
                   " Chrome/84.0.4147.105 Safari/537.36")
}


def getone(pid, url):
    response = requests.get(f"{url}&pid={pid}", headers=HEADERS)
    print(response)
    if response.status_code == 200:
        print(response.text)
    return response.text


def getcomment(pid, url):
    response = requests.get(f"{url}&pid={pid}", headers=HEADERS)
    # print(response)
    if response.status_code == 200:
        # print(response.text)
        return response.text
    else:
        raise Exception('no comment')


def getlist(p, url):
    response = requests.get(f"{url}&p={p}", headers=HEADERS)
    # print(response)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"getlist action fail, response is :\n{response}")


def spider_one_page(page, getcomment_url, folder, pid_list):
    """对单个页面进行爬取, 并将数据存储到文件中

    Args:
        page: str, api请求后获取的文本.
        comment_url: 获取评论api接口.
        folder: 存储文件的目录.
        end: 爬取帖子id最小值
        start: 爬取帖子id最大值
    Returns:
        max_pid, min_pid: 该页面pid最大最小值
    """
    page = json.loads(page, encoding='utf-8')
    page_data = page['data']
    if page_data != []:
        for post in page_data:
            pid = post['pid']
            if pid not in pid_list:
                comment = getcomment(pid, getcomment_url)
                post['comment'] = json.loads(comment, encoding='utf-8')
                dst = os.path.join(folder, f"{pid}.json")
                with open(dst, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(post, ensure_ascii=False))
    
        pid_list = [int(x['pid']) for x in page_data]
        return max(pid_list), min(pid_list)
    else:
        return -1, -1