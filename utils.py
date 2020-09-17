import requests
import json
import os
import threading


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


def spider_one_page(p, getlist_url, folder, pid_list=None):
    """对单个页面进行爬取, 并将数据存储到文件中.

    Args:
        p (int): 获取第p页的帖子.
        comment_url (str): 获取评论api接口.
        folder (str): 存储文件的目录.
        pid_list (list [int]): 已有的帖子id列表.
    Returns:
        pid_list (list [int]): 该页中包含读取帖子id列表.
    """
    page = getlist(p, getlist_url)
    page = json.loads(page, encoding='utf-8')
    page_data = page['data']
    if pid_list is None:
        pid_list = []
    post_list = filter(lambda x: int(x['pid']) not in pid_list, page_data)
    post_list = list(post_list)
    def post_dump(post):
        # 包装为小线程
        pid = post['pid']
        
        # comment = getcomment(pid, getcomment_url)
        # post['comment'] = json.loads(comment, encoding='utf-8')
        dst = os.path.join(folder, f"{pid}.json")
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(json.dumps(post, ensure_ascii=False))
        # print(f"pid: {pid} post download done")
    for post in post_list:
        t = threading.Thread(target=post_dump, args=(post, ))
        t.start()
    return [x['pid'] for x in post_list]


def spider_comments(pid_list, getcomment_url, folder):
    """多线程根据id列表爬取对应的评论，并将其存入json文件.

    Args:
        pid_list (list [int]): 需要爬取的pid文件.
        getcomment_url (str): 获取评论接口api.
        folder (str): 存储文件目录.
    Raises:
        AssertError: pid_list中数目超过最大容许的数目.
    """
    assert len(pid_list) <= 30, "pid list中的id数不得高于30"

    def comment_dump(pid):
        """ 根据pid获取单个评论内容，并保存
        """
        commment = getcomment(pid, getcomment_url)
        
        with open(os.path.join(folder, f"c{pid}.json"), 'w', encoding='utf-8') as f:
            f.write(commment)
    for pid in pid_list:
        t = threading.Thread(target=comment_dump, args=(pid, ))
        t.start()
    