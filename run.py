import requests
from urllib.parse import urlencode
from pyquery import PyQuery
from pymongo import MongoClient


base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['weibo_1']
collection = db['weibo']
max_page = 10

def get_page(page):
    '''
    获取源码
    :param page: 页数
    :return:
    '''
    params = {
        'type': 'uid',
        'value': '3024395081',
        'containerid': '1076033024395081',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), page
    except requests.ConnectionError as e:
        print(e.args)