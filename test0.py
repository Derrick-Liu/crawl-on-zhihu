#coding:utf-8
from lxml import etree
import requests
import re
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

url = 'https://www.zhihu.com/question/24861635'
url_post = 'https://www.zhihu.com/node/QuestionAnswerListV2'
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'}
headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'Content-Length': '93',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Xsrftoken': '7853674d11e9c10913a6a7fa508823a0',
        'Referer': 'https://www.zhihu.com/question/24861635',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'q_c1=65cd4da2853d4b53b932853b28e3b168|1483519932000|1483519932000; d_c0="AGDCBho_GguPTnNhvD21Ev6BbUuIfgufaGg=|1483519933"; _zap=823590fe-9fa0-40a2-889a-37d4a7d520fa; r_cap_id="YzliYTU1YzcyZjMwNGEzYzkyNjE4OWVmMzRhNmEzNWI=|1483521508|2a78a41624797f1b4996c5aea3eb2d119616c34b"; cap_id="NjliN2RmMzQzNWNjNDgyZGI3NTJmMzRlZjY5NWJjNGU=|1483529874|db0891f76f7c736adcefc983ce7e72fa1f8d2579"; l_cap_id="YmJhZDM2N2FjY2I3NDc0OWI4MjI1ZTk0OTRhZGZlMjY=|1483529874|cff65c288b1f4edacbd2348016c8a6e7568217eb"; login="NmZjNzY3ZjliMzFkNGY2ODg3YjZiNDA2Nzg4YmExOWY=|1483529874|13f7492442b7f3577d08751eff5294d93ef043c6"; _xsrf=7853674d11e9c10913a6a7fa508823a0; __utma=51854390.2127096924.1483519936.1483581447.1483582565.8; __utmc=51854390; __utmz=51854390.1483581447.7.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20160701=1^3=entry_date=20160701=1; z_c0=Mi4wQUNBQWN3NUZLUW9BWU1JR0dqOGFDeGNBQUFCaEFsVk5rbXVVV0FDc1VoWlBYWmhoMUZ0XzB0MTEyMGZ2dEQ2bTJn|1483595352|03fa3948472973f8bc580f116f07e7e642257bd5'
		}
data = 'method=next&params=%7B%22url_token%22%3A24861635%2C%22pagesize%22%3A10%2C%22offset%22%3A'+str(12)+'0%7D'
ajaxhtml = requests.post(url_post, data=data, headers=headers)   #ajax异步加载，返回str（形式上是dict）
dict_type = json.loads(ajaxhtml.content)              #变换json格式，结果为dict类型
list = dict_type['msg']                  #获得源代码的list，10个数据，每个数据为一个答主的源代码

f = open('info.txt', 'a')
for i in range(10):
    f.writelines(list[i])





# text=re.search(r'(<di class="answer-hed">.*?)<div id="zh-question-collapsed-link"',html,re.S)
#
# print text

# selector=etree.HTML(html)

# content=selector.xpath('//*[@id="zh-question-answer-wrap"]/div[1]')

# print content[0].child::text()
