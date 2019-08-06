import requests, json, urllib, sys
from requests.auth import HTTPBasicAuth
# from xml import etree
import xml.etree.ElementTree as at
base_url = "http://127.0.0.1:8000/api/v1/"
client = requests.session()
client.get(base_url)
if 'csrftoken' in client.cookies:
	csrftoken = client.cookies['name']
else:
	csrftoken = client.cookies['name']
# tree = etree.html(client.get(base_url).contact)
# tree = at.HTML_EMPTY

# csrf = tree.xpath("//input[@name='csrf_token']/@value")[0]

header = {
	"Content-Type":"application/json",
	"referer":base_url,

}
# headers = {
# 		'referer': base_url, 
# 		'content-type': 'application/x-www-form-urlencoded', 
# 		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# 		}
#use same session client
def login(urls, data):
	results = requests.post(base_url=+urls, data=json.dumps(data), headers=header)
	return {
				'data':results.text, 
				'status_code':results.status_code, 
				'simple_description':results.reason, 
				'method_user':results.request
			}

def register(urls, data):
	results = requests.post(base_url=+urls, data=json.dumps(data), headers=header)
	return {
				'data':results.text, 
				'status_code':results.status_code, 
				'simple_description':results.reason, 
				'method_user':results.request
			}

def create_object(urls, data):
	results = client.post(base_url+urls,auth=HTTPBasicAuth(username="admin", password="bags1234") , data=json.dumps(data), headers=header)
	return {
				'data':results.text, 
				'status_code':results.status_code, 
				'simple_description':results.reason, 
				'method_user':results.request
			}

def get_objects(urls):
	results = requests.get(base_url=+urls, headers=header)
	return {
				'data':results.text, 
				'status_code':results.status_code, 
				'simple_description':results.reason, 
				'method_user':results.request
			}
def delete_shop(urls):
	results = requests.delete(base_url+urls, headers=header)
	return {
				'data':results.text, 
				'status_code':results.status_code, 
				'simple_description':results.reason, 
				'method_user':results.request
			}

pres = {"username":"admin", "password":"bags1234"}
owner = login('login/', pres)
shop = {
	"name":"jangwe",
	"description":"keju iuiwu uhywieru iuhyiwu iuwioure uiweuo iuwoiuew",
	"location":"kampala uganda",
	"email":"jangwe@ugbags.app",
	"contact":"+256784567890"
}
data={"name":"uyhfyu hygrwyehd","description":"hvfe gvwwdyfg hygfyweuh yhgwuh","location":"jnikloi9pokplo0kio","contact": "+256788565455","email":"jijg@jgf.com"}
message = {"email":"ugbags@ugbags.app", "message":"huri uhyeuy uhyuweiw uhyuwe", "name":"no name","subject":"just an inquiry", 'csrfmiddlewaretoken':'csrftoken'}
print(create_object('contact/', message))

user_new = {
	"username":"aula",
	"email":"aula@ugbags.app",
	"password":"bags1234"
}
# print(get_objects('contact/'))