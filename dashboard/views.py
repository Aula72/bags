from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from dashboard.forms import (ContactForm, ShopForm, BagForm, AccountForm,
RegisterForm, LoginForm, ProfileForm)
import requests, json
from django.middleware.csrf import get_token 
from requests.auth import HTTPBasicAuth

base_url = "http://127.0.0.1:8000/api/v1/"
session = requests.Session()
def index(request):
	print(request.headers)
	messages = requests.get(base_url+'contact/')
	x = messages.json()	
	return render(request, 'dashboard/index.html', {'messages':x})
# Create your views here.

def contact(request):
	post_header = session.headers.update({
		"Content-Type":"application/json",
		"X-CSRFToken":get_token(request)
	})

	if request.method == 'GET':
		form = ContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		print(get_token(request))		
		if form.is_valid():
			name = form.data['name']
			email = form.data['email']
			message = form.data['message']
			subject = form.data['subject']
			mess ={
				"name":str(name), 
				"subject":str(subject),
				"email":str(email),
				"message":str(message)
			}
			requests.post(base_url+'contact/', json=mess,headers=post_header)
			# x.json()
		return render(request,'dashboard/index.html')
	return render(request, 'dashboard/contact.html', {
        'form': form,
    })

def accounts(request):
	account = requests.get(base_url+"financial-accounts/")
	acc = account.json()
	return render(request, 'dashboard/accounts.html', {'accounts':acc})

def shops(request):
	shop = requests.get(base_url+"shops/")
	return render(request, 'dashboard/shops.html', {"shops":shop.json()})
def create_shop(request):
	shop_headers =session.headers.update({
		"Content-Type":"application/json",
		"Authorization":"Token b80c7dd2e80799758cdffeb9ca6a4c6a711aa9b8",
		"X-CRSFToken":get_token(request)#obtaining csrf token from form
	})
	if request.method == 'GET':
		form = ShopForm()
	if request.method == 'POST':
		form = ShopForm(request.POST)
		if form.is_valid():
			name = form.data["name"]
			description = form.data["description"]
			location = form.data["location"]
			email = form.data["email"]
			contact = form.data["contact"]

			shop_data = {
				"name":name, "description":description, "location":location, "email":email, "contact":contact
			}
			shop_info = requests.post(base_url+"shops/", json=shop_data, headers=shop_headers)
			if shop_info.status_code==201:
				print("hehehehe")

	return render(request, 'dashboard/create_shop.html', {'form':form})
def shopdetails(request, pk):
	shop = requests.get(base_url+"shops/"+pk+"/")
	return render(request, 'dashboard/shop-details.html', {"shops":shop.json()})

def bags(request):
	bag = requests.get(base_url+"bags/")
	
	return render(request, 'dashboard/bags.html', {"bags":bag.json()})
def create_bag(request):
	bag_headers ={
		"Content-Type":"application/json",
		"X-CRSFToken":get_token(request)#obtaining csrf token from form
	}
	if request.method=='GET':
		form = BagForm()
	if request.method=='POST':
		form = BagForm(request.POST)
		if form.is_valid():
			price = form.data["price"]
			bag_type = form.data["bag_type"]
			bag_size = form.data["bag_size"]
			skin_type = form.data["skin_type"]
			bag_color = form.data["bag_color"]
			buying_type = form.data["buying_type"]
			image_one = form.data["image_one"]
			image_two = form.data["image_two"]
			image_three = form.data["image_three"]
			image_four = form.data["image_four"]
			simple_description = form.data["simple_description"]
			bag_data = {
				"price":price, "bag_type":bag_type, "bag_size":bag_size, "skin_type":skin_type,
				"bag_color":bag_color, "buying_type":buying_type,"image_one":image_one,
				'image_two':image_two, "image_three":image_three, "image_four":image_four,
				"simple_description":simple_description
			}
			bag_info = requests.post(base_url+"bags/", json=bag_data, headers=bag_headers)
			if bag_info.status_code == 201:
				print("iuf iu")
	return render(request, 'dashboard/create_bag.html', {'form':form})
def bagdetails(request, pk):
	bag = requests.get(base_url+"bags/"+pk+"/")
	return render(request, 'dashboard/bag-details.html', {"bags":bag.json()})

def accounts(request):
	account = requests.get(base_url+"financial-accounts/")
	return render(request, 'dashboard/accounts.html', {"accounts":account.json()})
def create_account(request):
	acc_headers =session.headers.update({
		"Content-Type":"application/json",
		"Authorization":"Token b80c7dd2e80799758cdffeb9ca6a4c6a711aa9b8",
		"X-CRSFToken":get_token(request)#obtaining csrf token from form
	})
	if request.method=='GET':
		form = AccountForm()
		print(acc_headers)
	if request.method == 'POST':
		form = AccountForm(request.POST)
		if form.is_valid():
			amount = form.data['amount']
			trans_type = form.data["transaction_type"]
			acc_data = {
				"amount":amount,
				"trans_type":trans_type
			}
			acc_info = requests.post(base_url+"accounts/", json=acc_data, headers=acc_headers)
			if acc_info.status_code == 201:
				print("yess")

	return render(request, 'dashboard/create_account.html', {'form':form})
def accountdetails(request, pk):
	account = requests.get(base_url+"financial-accounts/"+pk+"/")
	return render(request, 'dashboard/account-details.html', {"accounts":bag.json()})

def login(request):
	log_headers = {
		'User-agent': request.headers['User-Agent'],
		"Content-Type":"application/json",
		"X-CSRFToken":get_token(request)#obtain csrf_Token from the form
	}
	
	p = request.headers['User-agent']
	if request.method=='GET':
		print(request.headers['User-agent'])
		form = LoginForm()
		print(log_headers)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.data["username"]
			password = form.data["passwords"]
			log_data = {"username":str(username), "password":str(password)}
			log_info = requests.post(base_url+"login/", json=log_data,headers=log_headers)
			if log_info.status_code==200:
				print(request.user)
				tokens = json.loads(log_info.text)
				# request.headers.get()
				
				# session.auth(username, password)
				# request.user.
				# request.META['HTTP_AUTHORIZATION'] = 'WWW-Authorization: Token %s'%tokens["token"]
				# request.headers.set({'WWW-Authorization': "Token %s"%tokens["token"]})
				session.headers.update({'WWW-Authorization': "Token %s"%tokens["token"]})
				session.headers.update({'User-agent': p})
				print(session.headers.items())				
				# return HttpResponseRedirect(reverse('dashboard:index'))
				return render(request,'dashboard/index.html', {'headers':session.headers.items()})
				# return response
	return render(request, 'dashboard/login.html', {'form':form})

def register(request):
	reg_headers ={
		"Content-Type":"application/json",
		"X-CRSFToken":get_token(request)#obtaining csrf token from form
	}
	if request.method =='GET':
		form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			email = form.data["email"]
			password = form.data["password"]
			username = form.data["username"]
			reg_data = {
				"username":str(username),
				"password":str(password),
				"email":str(email)
			}
			reg_info = requests.post(base_url+"register/", json=reg_data, headers=reg_headers)
			if reg_info.status_code == 201:
				print("yes")
	return render(request, 'dashboard/register.html', {'form':form})

def logout(request):
	log_out = requests.post(base_url+'logout/')	
	if log_out.status_code==204:
		session.headers.clear()
		response = render_to_response('dashboard/index.html',{},RequestContext(request))
		response.delete_cookie('user_logged')
		return response
	return HttpResponseRedirect(reverse('dashboard:index'))
	
def profile(request):
	prof_headers = {
		"Content-Type":"application/json",
		"X-CRSFToken":get_token(request)#obtaining csrf token from form
	}
	if request.method == 'GET':
		form = ProfileForm()
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			nin = form.data["nin"]
			gender = form.data["gender"]
			email = form.data["email"]
			photo = form.data["photo"]
			user_type = form.data["user_type"]
			print(type(photo), type(email))
			prof_data = {
				"nin":str(nin),
				"User_type":str(user_type),
				"photo":photo,
				"email":str(email),
				"gender":str(gender)
			}
			prof_info = requests.post(base_url+"profile/",json=prof_data, headers=prof_headers)
			if prof_info.status_code == 201:
				print("oroie ijer")
			
	return render(request, 'dashboard/profile.html', {'form':form})