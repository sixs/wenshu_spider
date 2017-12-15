import requests
from urllib import parse
import execjs
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')		#改变标准输出的默认编码
session = requests.Session()


def get_guid():
	#获取guid参数
	js1 = '''
		function getGuid() {
	        var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
	       	return guid;
	    }
	    var createGuid = function () {
	        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
	    }
	'''
	ctx1 = execjs.compile(js1)
	guid = (ctx1.call("getGuid"))
	return guid

def get_number(guid):
	###获取number
	codeUrl = "http://wenshu.court.gov.cn/ValiCode/GetCode"
	data = {
		'guid':guid
	}
	req1 = session.post(codeUrl,data=data)
	number = req1.text
	return number

def get_vjkl5(guid,number):
	####获取cookie中的vjkl5
	url1 = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number="+number+"&guid="+guid+"&conditions=searchWord+QWJS+++"+parse.quote(Param)
	Referer1 = url1
	headers1 = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Host":"wenshu.court.gov.cn",
		"Proxy-Connection":"keep-alive",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
	}
	req1 = session.get(url=url1,headers=headers1)
	vjkl5 = req1.cookies["vjkl5"]
	return vjkl5

def get_vl5x(vjkl5):
	#根据vjkl5获取参数vl5x
	js = ""
	fp1 = open('./sha1.js')
	js += fp1.read()
	fp1.close()
	fp2 = open('./md5.js')
	js += fp2.read()
	fp2.close()
	fp3 = open('./base64.js')
	js += fp3.read()
	fp3.close()
	fp4 = open('./vl5x.js')
	js += fp4.read()
	fp4.close()
	ctx2 = execjs.compile(js)
	vl5x = (ctx2.call('vl5x',vjkl5))
	return vl5x


def get_data(Param,Index,Page,Order,Direction):
	guid = get_guid()
	number = get_number(guid)
	vjkl5 = get_vjkl5(guid,number)
	vl5x = get_vl5x(vjkl5)

	#获取数据
	url2 = "http://wenshu.court.gov.cn/List/ListContent"
	headers2 = {
		"Accept":"*/*",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
		"Host":"wenshu.court.gov.cn",
		"Origin":"http://wenshu.court.gov.cn",
		"Proxy-Connection":"keep-alive",
		# "Referer":Referer1,
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
		"X-Requested-With":"XMLHttpRequest"
	}
	data = {
		"Param":Param,
		"Index":Index,
		"Page":Page,
		"Order":Order,
		"Direction":Direction,
		"vl5x":vl5x,
		"number":number,
		"guid":guid
	}
	req2 = session.post(url=url2,headers=headers2,params=data)
	data = json.loads(req2.text)
	print(data)

#搜索条件
Param = "全文检索:*"	#搜索关键字
Index = 1		#第几页
Page = 20		#每页几条
Order = "法院层级"	#排序标准
Direction = "asc"	#asc正序 desc倒序


get_data(Param,Index,Page,Order,Direction)
