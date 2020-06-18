import redis
import requests,json

from commons import fisco_utils
from tornado import auth
host = 'http://192.168.1.119:6001/weid/api/invoke'
#
from actions.backoffice.weid_request_args import Args
#
# header={'Content-Type:'}

# print(res.json())
from threading import Thread

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r.hset('stu','name','jj')
# print(r.hgetall('stu'))
# import io
import ipfshttpclient
# 连接IPFS，需要先启动节点服务器daemon
# chunk_size 上传大小限制 这里10M
# w = io.BytesIO()
# w.write(bytes('hello world','utf8'))
# v = w.getvalue()
# print(v)
# api = ipfshttpclient.connect('/ip4/183.2.223.53/tcp/5001/http')
# lst = [1,2,'lol']
# res = api.add_json(lst)
# print(res)
# s = api.get_json('QmfXwvjtRqznruRptDaoUWFoviUZgGsz1BjVRRCWxQAsfb')
# print(s)
# url_link = api.add_bytes(v)
# print(url_link)
# fisco_client = fisco_utils.Client('test1', '0x73abb55230ad251b9bf2cf3fcce8d27130750d53')
# res = fisco_client.fisco_add_data('createSubject', ['20200621','did:weid:1:0x685e69ba2202faa5b232eb1e7c1467699c8fa74b',20200621,120 ])
# print(res)
a = ([3,4],[1,2])
c= list(a)
print(c)
b =[5,6]
list(a).append(b)
print(a)