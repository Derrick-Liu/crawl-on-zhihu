# coding:utf-8
import requests
import re
import json
import urllib
from lxml import etree
from multiprocessing.dummy import Pool
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Crawl:
	def __init__(self):
		pass
		
	def getDataInPost(self):
		dataList=[None]
		for i in range(1,35):
			data = 'method=next&params=%7B%22url_token%22%3A24861635%2C%22pagesize%22%3A10%2C%22offset%22%3A'+str(i)+'0%7D'
			dataList.append(data)
		return dataList
	
	def getHTML(self,urlinput, data):
		if not data:
			header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'}
			html = requests.get(url,headers=header).content
			return html
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
		ajaxhtml = requests.post(urlinput, data=data, headers=headers)   #ajax异步加载，返回str（形式上是dict）
		dict_type = json.loads(ajaxhtml.content)              #变换json格式，结果为dict类型
		list = dict_type['msg']                  #获得源代码的list，10个数据，每个数据为一个答主的源代码
		return list    #html
		
	def getImage(self,html):
		if type(html) is not 'str':
			html=''.join(html)                   #非第一页返回是list
		list=re.findall('data-original="(.*?)"', html)
		for i in range(0, len(list) - 1, 2):
			print list[i]
			# filename = list[i].split('/')[-1]
			# urllib.urlretrieve(list[i], 'loads/%s' % filename)

	def getInfo(self,html):
		infoList=[]
		for i in range(len(html)):
			info={}
			object=re.search(r'<span class="name">(.*?)</span>',html[i],re.S)
			if not object:
				info['name']=re.search(r'target="_blank" href="/people/.*?>(.*?)</a></span>',html[i],re.S).group(1)
				signature=re.search(r'span title="(.*?)" class="bio"',html[i],re.S)
				if signature:
					info['signature']=signature.group(1)
				else:
					info['signature']='No infomation'
				info['homepage']='https://www.zhihu.com'+re.search(r'target="_blank" href="(/people/.*?)"',html[i],re.S).group(1)
			else:
				info['name'] =object.group(1)
				info['signature']='No infomation'
				info['homepage']='No infomation'

			approval=re.search(r'<span class="js-voteCount">(.*?)</span>',html[i],re.S)
			if approval:
				info['approval']=approval.group(1)+' approvals'
			else:
				info['approval']='0 approval'

			comments=re.search(r'<i class="z-icon-comment"></i>(.*?)</a>',html[i],re.S)
			if comments:
				info['comments']=comments.group(1)+' comments'
			else:
				info['comments']='0 comments'

			print info
			infoList.append(info)
		return infoList

	def saveInfo(self,infoList):
		f = open('info.txt', 'a')
		for each in infoList:
			f.writelines('name: '+each['name']+'\n')
			f.writelines('homepage: '+each['homepage']+'\n')
			f.writelines('signature: '+each['signature']+'\n')
			f.writelines('approval: '+each['approval']+'\n')
			f.writelines('comments: '+each['comments']+'\n\n')
		f.close()


if __name__ == '__main__':
	url = 'https://www.zhihu.com/question/24861635'
	url_post = 'https://www.zhihu.com/node/QuestionAnswerListV2'
	cookie = {
		"Cookie": 'q_c1=65cd4da2853d4b53b932853b28e3b168|1483519932000|1483519932000; _xsrf=85f7e963dd2119f4b8c73df4e132422a; d_c0="AGDCBho_GguPTnNhvD21Ev6BbUuIfgufaGg=|1483519933"; _zap=823590fe-9fa0-40a2-889a-37d4a7d520fa; r_cap_id="YzliYTU1YzcyZjMwNGEzYzkyNjE4OWVmMzRhNmEzNWI=|1483521508|2a78a41624797f1b4996c5aea3eb2d119616c34b"; cap_id="NjliN2RmMzQzNWNjNDgyZGI3NTJmMzRlZjY5NWJjNGU=|1483529874|db0891f76f7c736adcefc983ce7e72fa1f8d2579"; l_cap_id="YmJhZDM2N2FjY2I3NDc0OWI4MjI1ZTk0OTRhZGZlMjY=|1483529874|cff65c288b1f4edacbd2348016c8a6e7568217eb"; login="NmZjNzY3ZjliMzFkNGY2ODg3YjZiNDA2Nzg4YmExOWY=|1483529874|13f7492442b7f3577d08751eff5294d93ef043c6"; n_c=1; z_c0=Mi4wQUNBQWN3NUZLUW9BWU1JR0dqOGFDeGNBQUFCaEFsVk5rbXVVV0FDc1VoWlBYWmhoMUZ0XzB0MTEyMGZ2dEQ2bTJn|1483529912|c3ca63703101356f57eda7325e29c81c761a75a2; __utma=51854390.2127096924.1483519936.1483519942.1483529919.3; __utmb=51854390.0.10.1483529919; __utmc=51854390; __utmz=51854390.1483529919.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20160701=1^3=entry_date=20160701=1'}

	spider = Crawl()
	dataLi = spider.getDataInPost()
	#循环遍历所有源代码
	for i in range(35):  #len(dataLi)):
		print '正在处理第%d页数据'%(i+1)
		if dataLi[i] is None:
			html = spider.getHTML(url, dataLi[i])
		else:
			html = spider.getHTML(url_post, dataLi[i])
			infoList = spider.getInfo(html)
			spider.saveInfo(infoList)
		spider.getImage(html)
