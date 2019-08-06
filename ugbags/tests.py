import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','ugbags.`settings`')
from rest_framework.test import  APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse

# client = APIClient()
# base_url = 'http://127.0.0.1:8000/api/v1/'
# def post_data(urls, datas):
# 	client.post(base_url+urls, datas, format='json')

x={"name":"aula simon", "email":"aula.simon@ugbags.app","subject":"my details","message":"these are my details just know for now!"}
# post_data('contact/', x)

class ContactTests(APITestCase):
	url = reverse('ugbags:contact-list')
	response = self.client.post(url, x, format=json)
	self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	self.assertEqual(response.data, data)
