import json
import time
from pymongo import MongoClient
import requests
from lxml import etree

class Mhxy(object):

    def __init__(self, page):
        self.page = page
        self.time = str(int(time.time()*1000))
        self.url = 'https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&level_min=69&level_max=69&school=10&server_type=3&act=recommd_by_role&page={1}&count=15&search_type=overall_search_role&view_loc=overall_search'.format(self.time, page)
        self.headers = {

            'Referer': 'https://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py',

            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        # self.data = {
        #     'school': 10
        # }

        self.client = MongoClient('127.0.0.1', 27017)

        # 选择一个数据库
        self.db = self.client['admin']

        # 这里是认证登录所以需要进入admin进行登录
        self.db.authenticate('yzs', 'yy961124')

        # 选择一个集合
        self.col = self.client['test']['mhxy']
        self.info = 'fingerprint=h8od8au5qfxnorfv; __session__=1; _ntes_nnid=3ebc92c136d0119b371c7c0a1189a0bf,1574054665941; _ntes_nuid=3ebc92c136d0119b371c7c0a1189a0bf; no_login_mark=1; cbg_qrcode=ydc6720jfM0Cgxl5iCo_3w_SHmCvcpl20GdksQBg; cur_servername=%25E7%258F%258D%25E5%25AE%259D%25E9%2598%2581; _9755xjdesxxd_=32; YD00000722197596%3AWM_NI=gqxBtA9lpnA4FDMUhpVj2Uza6MhBxRE%2Fk8JrwjMUkmn6IsqF51El5O7flzze6wFRVjNX3lAGtPR0l7Rw16wxmlEcKPcUfIwV7IaHEvpjUSRnsWTHIeL0dxqTEf9bjxtIWGg%3D; YD00000722197596%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb3f34eab9cfbd7ef5ab1b88ba3d45a878f8eaef23e9ceab7aef84bf88aaeb6f42af0fea7c3b92aa5afb8a3f74bfbb4c08fc440869c83b6eb7c96b6feb6f96bf693a8a3fb5a87f1a5d9c97ab5b683b6ea67aeea8794f44ef7ef8b8db845f5baa49bf96ff6a98ab3d5628e88fd8dc44db8909ed1ef3d92a9ffd7f674afb48b84ca5ca18baaaaf65ef597afa9c87eb4b69bb4d166b1899ca9cc6f90f0ac99f46087baf783e974b89799a8e637e2a3; YD00000722197596%3AWM_TID=vF0a5D4Q46RBQEAAQQN97T6mIrRsFeQr; wallet_data=%7B%22is_locked%22%3A%20false%2C%20%22checking_balance%22%3A%200%2C%20%22balance%22%3A%200%2C%20%22free_balance%22%3A%200%7D; area_id=4; NTES_SESS=6Z6mQi15zIt.v11zNSo98u3Vdt9MtZocfpzP9HFrkppp0Ea_8hud7bWtWNxXLBNMA9VkfKLqFnN4LaXptOlT8I4.nr.gK4qZo6MxUChyyWzMoPYSpBFv9RBlf1AXhghme2hVv8kk6dxOibNXRvlNpAkELNM.TtFH46BGuvuTHwL5NH4m8s15TU1fbGjeNvvbBSH_PWfLz.inAI1hiYlDMiBXM; S_INFO=1574066191|0|3&80##|m18861816385; P_INFO=m18861816385@163.com|1574066191|0|cbg|00&99|shh&1574066160&cbg#shh&null#10#0#0|176530&0|cbg|17626960530@163.com; sid=OHmNF0sP3P_HDx7UbFwjGikXcRUBSNB-I4wzy8i2; last_login_roleid=32312910; login_user_nickname=%25E5%2588%25AB%25E6%2589%2593%25E6%2584%259F%25E6%2583%2585%25E7%2589%258C; is_user_login=1; login_user_icon=203; login_user_roleid=32312910; login_user_level=30; login_user_urs=m18861816385@163.com; login_user_school=3; new_msg_num=13; offsale_num=0; unpaid_order_num=0; unpaid_order_price_total=0.00; last_login_role_serverid=358; recommend_typeids=1,2,3,4; recommend_url=https://xyq.cbg.163.com/cgi-bin/query.py?act=recommend_search&recommend_type=1; last_login_serverid=358; remind_offsale=1; alert_msg_flag=1; gdxidpyhxdE=9%5ClGbjBWJpi2eEc%2BkXBtCvjRse6CW5B4BLvyMBgR4%2B5e%2F23aTaq%2FPgzgGocS2MMxVznROs0BghIZyEk2d%2B%2BOPE2xyVrGwnibVca5a7xNMjYeWJ0GqPos%2Bdqw%2B5yIpZ2C%2FSxQOkjGRLJD35goyh4hEShp%5CUZwE84uTc6baNbr1XQljElP%3A1574068444473'
        self.cookie = {cookie.split('=')[0]: cookie.split('=')[-1]for cookie in self.info.split(';')}

        self.data = {

            '_': self.time,
            'level_min': '69',
            'level_max': '69',
            'school': '10',
            'server_type': '3',
            'act': 'recommd_by_role',
            'page': self.page,
            'count': '15',
            'search_type': 'overall_search_role',
            'view_loc': 'overall_search',
        }

    def request_url(self):

        response = requests.get(self.url, headers=self.headers, cookies=self.cookie, params=self.data)

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
            self.col.insert(value)
            print('插入第{0}页,第{1}条数据成功'.format(self.page, index+1))


    def run(self):


        role = self.request_url()
        self.save(role)




if __name__ == '__main__':

    for i in range(45, 70):

        a = Mhxy(i)
        time.sleep(5)
        a.run()