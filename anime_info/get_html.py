"""
WEBサイトのHTMLを取得して標準出力するプログラム
開発時にWEBサイトのアクセス回数を減らすために使用
"""

import requests

target_url = 'https://akiba-souken.com/anime/summer/'
response = requests.get(target_url)
print(response.text)
