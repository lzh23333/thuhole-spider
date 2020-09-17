import json
from utils import getlist

with open('config.json', 'r') as f:
    config = json.load(f)
getlist_url = (f"{config['api_url']}&action=getlist"
               f"&user_token={config['user_token']}")
a = getlist(1500, getlist_url)
print(a)