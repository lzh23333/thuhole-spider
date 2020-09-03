import requests


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

