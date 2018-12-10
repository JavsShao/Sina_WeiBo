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

def parse_page(json, page:int):
    '''
    解析源码
    :param json:
    :param page:
    :return:
    '''
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog', {})
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['内容'] = PyQuery(item.get('text')).text()
                weibo['点赞数'] = item.get('attitudes_count')
                weibo['评论数'] = item.get('comments_count')
                weibo['转发量'] = item.get('reposts_count')
                yield weibo

def save_to_mongo(result):
    '''
    保存结果到Mongodb数据库中
    :param result:
    :return:
    '''
    if collection.insert(result):
        print('保存到mongodb数据库中.....')

if __name__ == '__main__':
    for page in range(1, max_page + 1):
        json = get_page(page)
        results = parse_page(*json)
        for result in results:
            print(result)
            save_to_mongo(result)