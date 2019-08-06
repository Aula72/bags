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



