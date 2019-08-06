import requests, json

urls = 'http://127.0.0.1:8000/'
client = requests.session()

client.get(urls)
csrftoken = client.cookies['csrftoken']

submit_data = {
    "username":"admin",
    "password":"bags1234",
    "csrfmiddlewaretoken":str(csrftoken)
}

'''
my-key:e24cc65c3c88f96e1402ffc54b7713087bd3df49
'''

