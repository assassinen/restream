import requests
from model.product import Product
import os.path
import jsonpickle

class Rest:

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.search_url = base_url.format('rest', 'product', 'search')
        self.username = username
        self.password = password
        self.login()
        self.basketItem = []
        self.basketItemId = []


    def login(self):
        data = {'email': self.username, 'password': self.password}
        url = self.base_url.format('rest','user', 'login')
        responce = requests.post(url, json=data)
        if responce.status_code == 200:
            self.basket_id = responce.json()['authentication']['bid']
            self.token = responce.json()['authentication']['token']
            self.basket_url = self.base_url.format('rest', 'basket', self.basket_id)
            self.headers = {'Authorization': 'Bearer {}'.format(self.token)}


    def get_status_code(self, pattert = ''):
        self.search(pattert)
        return self.status_code


    def search(self, pattert = ''):
        url = self.search_url + '?q=' + pattert
        responce = requests.get(url)
        self.status_code = responce.status_code
        if responce.status_code == 200:
            return responce.json()['data']


    def get_product_list(self, pattert = ''):
        list=[]
        products = self.search(pattert)
        for product in products:
            (id, name, description, price, image, _, _, _) = product.values()
            product_kwargs = dict(zip(['id', 'name', 'description', 'price', 'image'], [id, name, description, price, image]))
            list.append(Product(**product_kwargs))
        return list


    def load_from_json(self, file):
        testdata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)
        with open(testdata_file) as f:
            return jsonpickle.decode(f.read())


    def get_basket_items(self):
        responce = requests.get(url=self.basket_url, headers=self.headers)
        if responce.status_code == 200:
            return responce.json()['data']['products']


    def add_product(self, product=None):
        if product is None:
            return False

        self.basketItem = {i['basketItem']['ProductId']: i['basketItem']['quantity'] for i in self.get_basket_items()}
        self.basketItemId = {i['basketItem']['ProductId']: i['basketItem']["id"] for i in self.get_basket_items()}
        product_id = product.id_or_max()
        if product_id not in self.basketItem:
            quantity = 1
            data = {"ProductId": product_id, "BasketId": self.basket_id, "quantity": quantity}
            url = self.base_url.format('api', 'BasketItems', '')
            responce = requests.post(url, json=data, headers=self.headers)
        else:
            quantity = self.basketItem[product_id] + 1
            basketItemId = self.basketItemId[product_id]
            data = {"quantity": quantity}
            url = self.base_url.format('api', 'BasketItems', basketItemId)
            responce = requests.put(url, json=data, headers=self.headers)

        if responce.status_code == 200:
            return True



    def get_basket_products(self):
        list = []
        products = self.get_basket_items()
        for product in products:
            (id, name, description, price, image, _, _, _, _) = product.values()
            product_kwargs = dict(zip(['id', 'name', 'description', 'price', 'image'], [id, name, description, price, image]))
            list.append(Product(**product_kwargs))
        return list





    # def logout(self):
    #     wd = self.app.wd
    #     self.app.open_home_page()
    #     wd.find_element_by_link_text("Logout").click()


# url = "https://restream.sloppy.zone/rest/user/login"
#
#
# data = {'email': 'restream34@mailinator.com', 'password': 'qwerty'}
#
# # with open('binary_data_file.bin','w') as f:
# #     f.write(data)
#
# print(data)
# # print(data)
# res = requests.post(url=url, json=data)
#
# print(res.status_code)
# print(res.text)


# r = requests.post("http://indegy.qtestnet.com/api/login",data="j_username= maxmccloud%40qasymphony.com&j_password=p@ssw0rd")
# print r.text



# # curl 'https://restream.sloppy.zone/rest/user/login' -H 'Pragma: no-cache' -H 'Origin: https://restream.sloppy.zone' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' -H 'Content-Type: application/json;charset=UTF-8' -H 'Accept: application/json, text/plain, */*' -H 'Cache-Control: no-cache' -H 'Referer: https://restream.sloppy.zone/' -H 'Cookie: io=8_CDyZ9NNyEWAHeFAABm' -H 'Connection: keep-alive' --data-binary '{"email":"restream34@mailinator.com","password":"qwerty"}' --compressed
#
# POST /rest/user/login HTTP/1.1
# Host: restream.sloppy.zone
# Connection: keep-alive
# Content-Length: 57
# Pragma: no-cache
# Cache-Control: no-cache
# Accept: application/json, text/plain, */*
# Origin: https://restream.sloppy.zone
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
# Content-Type: application/json;charset=UTF-8
# Referer: https://restream.sloppy.zone/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
# Cookie: io=8_CDyZ9NNyEWAHeFAABm
#
#
# https://restream.sloppy.zone/rest/user/login
#
# {"authentication":{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6OSwiZW1haWwiOiJyZXN0cmVhbTM0QG1haWxpbmF0b3IuY29tIiwicGFzc3dvcmQiOiJkODU3OGVkZjg0NThjZTA2ZmJjNWJiNzZhNThjNWNhNCIsImNyZWF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCJ9LCJpYXQiOjE1MzI5NjE4NjUsImV4cCI6MTUzMjk3OTg2NX0.k-xoPzNyzawQcU_84sa6nwuOfIb6rHtVZzH0SWw8hXg","bid":6,"umail":"restream34@mailinator.com"}}

# import requests
# from lxml import html

# url = 'http://classic.dzzzr.ru/moscow/'
#
# r = requests.get(url=url)
#
# cookies = {'b': 'b',
#            '__cfduid': r.cookies['__cfduid'],
#            'hotlog': '1'}
#
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#            'Accept-Encoding': 'gzip, deflate',
#            'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6,es;q=0.4',
#            'Cache-Control': 'no-cache',
#            'Connection': 'keep-alive',
#            'Content-Length': '43',
#            'Content-Type': 'application/x-www-form-urlencoded',
#            'Host': 'classic.dzzzr.ru',
#            'Origin': 'http://classic.dzzzr.ru',
#            'Pragma': 'no-cache',
#            'Referer': 'http://classic.dzzzr.ru/moscow/',
#            'Upgrade-Insecure-Requests': '1',
#            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
#
# data = {'action': 'auth', 'login': '<login>', 'password': '<password>'}
#
# r = requests.post(url='http://classic.dzzzr.ru/moscow/', cookies=cookies, headers=headers, data=data,
#                   allow_redirects=False)
#
# cookies['dozorSiteSession'] = r.cookies['dozorSiteSession']
#
# r = requests.get('http://classic.dzzzr.ru/moscow/?section=teamsettings', cookies=cookies)
# tree = html.fromstring(r.content)
#
# players = [x.text for x in tree.cssselect('tr[valign]:nth-child(10) td:nth-child(2) a')]
# for player in players:
#     print(player)


# curl
# 'https://restream.sloppy.zone/rest/basket/6'
# -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br'
# -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://restream.sloppy.zone/'
# -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6OSwiZW1haWwiOiJyZXN0cmVhbTM0QG1haWxpbmF0b3IuY29tIiwicGFzc3dvcmQiOiJkODU3OGVkZjg0NThjZTA2ZmJjNWJiNzZhNThjNWNhNCIsImNyZWF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCJ9LCJpYXQiOjE1MzI5NjQxNzcsImV4cCI6MTUzMjk4MjE3N30.RAVxUWZS3nmkBCd_y3M49ttHBoY3B8HlUQj9-55vneY'
# -H 'Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6OSwiZW1haWwiOiJyZXN0cmVhbTM0QG1haWxpbmF0b3IuY29tIiwicGFzc3dvcmQiOiJkODU3OGVkZjg0NThjZTA2ZmJjNWJiNzZhNThjNWNhNCIsImNyZWF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCJ9LCJpYXQiOjE1MzI5NjQxNzcsImV4cCI6MTUzMjk4MjE3N30.RAVxUWZS3nmkBCd_y3M49ttHBoY3B8HlUQj9-55vneY; io=tzKOG4PcA5TeW2-RAABp'
# -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed

# headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6OSwiZW1haWwiOiJyZXN0cmVhbTM0QG1haWxpbmF0b3IuY29tIiwicGFzc3dvcmQiOiJkODU3OGVkZjg0NThjZTA2ZmJjNWJiNzZhNThjNWNhNCIsImNyZWF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMTgtMDctMjAgMDg6NDA6MDEuMDAwICswMDowMCJ9LCJpYXQiOjE1MzI5NjQxNzcsImV4cCI6MTUzMjk4MjE3N30.RAVxUWZS3nmkBCd_y3M49ttHBoY3B8HlUQj9-55vneY'}
#
# url = 'https://restream.sloppy.zone/rest/basket/6'
# r = requests.get(url=url, headers=headers)
# # print(r.json()['data']['products'][0].keys())
# for i in r.json()['data']['products']:
#     for k, v in i.items():
#         print(k, v)
