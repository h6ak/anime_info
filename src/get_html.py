import requests

target_url = 'https://akiba-souken.com/anime/summer/'
response = requests.get(target_url)
print(response.text)
