import json
import random
import time
from pymongo import MongoClient
import requests


from header import get_request_header


class Mhxy(object):

    def __init__(self, page):
        self.page = page
        self.time = str(int(time.time()*1000))
        # _=代表时间戳, level分别代表了两个等级区间, server_type为定值不变, page页码, 其余定值不变, 如果需要指定门派可以增加school参数
        self.url = 'https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&level_min=175&level_max=175&server_type=3&act=recommd_by_role&page={1}&count=15&search_type=overall_search_role&view_loc=overall_search'.format(self.time, page)
        self.headers = get_request_header()


        self.bproxy = requests.get('http://118.25.93.211:16688/random?protocol=http&nick_type=2', headers=self.headers)
        self.proxy = {
            'http': self.bproxy.content.decode()
        }


        self.client = MongoClient('127.0.0.1', 27017)

        # 选择一个数据库
        self.db = self.client['admin']

        # 这里是认证登录所以需要进入admin进行登录, 不使用auth认证登录的mongo可以忽略
        self.db.authenticate('yzs', 'yy961124')

        # 选择一个集合
        self.col = self.client['test']['175_mhxy']
        self.info = 'return_url=; _ntes_nnid=510cab6547aa0e440af816dde796c00d,1576391392098; _ntes_nuid=510cab6547aa0e440af816dde796c00d; fingerprint=u8xbeja3vzkavszi; __session__=1; area_id=1; cbg_qrcode=dX-NS21tu_SXXA547UqK9iw1sQbqOyIq6AhO86u2; sid=yVKAKllBcWusoGzN3RaSMdi9XVKJHMDjkYVbIHT5; cur_servername=%25E7%258F%258D%25E5%25AE%259D%25E9%2598%2581; wallet_data=%7B%22is_locked%22%3A%20false%2C%20%22checking_balance%22%3A%200%2C%20%22balance%22%3A%200%2C%20%22free_balance%22%3A%200%7D; last_login_roleid=32312910; login_user_nickname=%25E5%2588%25AB%25E6%2589%2593%25E6%2584%259F%25E6%2583%2585%25E7%2589%258C; is_user_login=1; login_user_icon=203; login_user_roleid=32312910; login_user_level=30; login_user_urs=m18861816385@163.com; login_user_school=3; new_msg_num=13; offsale_num=0; unpaid_order_num=0; unpaid_order_price_total=0.00; last_login_role_serverid=358; recommend_typeids=1,2,3,4; recommend_url=https://xyq.cbg.163.com/cgi-bin/query.py?act=recommend_search&recommend_type=1; last_login_serverid=358; remind_offsale=1; alert_msg_flag=1'
        self.cookie = {cookie.split('=')[0]: cookie.split('=')[-1]for cookie in self.info.split(';')}


    def request_url(self):

        response = requests.get(self.url,   headers=self.headers, proxies=self.proxy)
        time.sleep(random.uniform(1, 3))
        data_dict = json.loads(response.content.decode())
        role = []
        for data in data_dict['equips']:
            role_dict = {}
            highlight = []
            role_dict['role_name'] = data['seller_nickname']
            role_dict['role_id'] = data['seller_roleid']
            role_dict['role_price'] = data['price']
            role_dict['role_level'] = data['equip_level_desc']
            role_dict['server_name'] = data['server_name']
            role_dict['role_selling_time'] = data['selling_time']
            role_dict['role_time_left'] = data['time_left']
            role_dict['role_link'] = 'https://xyq.cbg.163.com/equip?s={0}&eid={1}'.format(data['server_id'], data['eid'])
            highlights = data['highlights']if data['highlights'] else ''
            if highlights:
                for i in highlights:
                    highlight.append(i[0])
            role_dict['highlights'] = highlight
            role.append(role_dict)
        return role

    def save(self, role):

        for index, value in enumerate(role):
            count = self.col.count_documents({'_id': value['role_name']})
            if count == 0:
                dict = value
                dict['_id'] = value['role_name']
                self.col.insert(dict)
                print('插入第角色:{}'.format(value['role_name']))
            else:
                print('已存在角色:{}'.format(value['role_name']))


    def run(self):


        role = self.request_url()
        self.save(role)




if __name__ == '__main__':

    for i in range(1, 110):

        a = Mhxy(i)
        time.sleep(random.uniform(3, 6))
        a.run()