from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as login_to_django, logout as logout_to_django

from rest_framework import (status, generics, permissions, 
							renderers, exceptions, authentication)
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import (api_view, action, permission_classes, 
										authentication_classes)
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


from ugbags.models import Bag, Shop, Profile, Contact, Account
from django.contrib.auth.models import User
from ugbags.serializers import (BagSerializer, UserSerializer, 
	ShopSerializer, ProfileSerializer,ContactSerializer, LoginSerializer, AccountSerializer, EverythingSerializer)

from ugbags.permissions import IsOwnerOrReadOnly
#api url root
@api_view(['GET'])
def api_root(request, format=None):
	"""
	Ugbags API Root Endpoint
	
	Returns all available API endpoints with their URLs.
	This is the main entry point for discovering all API resources.
	"""
	return Response({
		'bags':reverse('ugbags:bag-lists', request=request, format=format),
		'shops':reverse('ugbags:shop-list', request=request, format=format),
		'users':reverse('ugbags:user-list', request=request, format=format),
		'profiles':reverse('ugbags:profile-list', request=request, format=format),
		'financial-accounts':reverse('ugbags:account-list', request=request, format=format),
		'login':reverse('ugbags:login', request=request, format=format),
		'logout':reverse('ugbags:logout', request=request, format=format),
		'register':reverse('ugbags:account-create', request=request, format=format),
		'search':reverse('ugbags:search-results', request=request, format=format),
		})
class CsrfExceptSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return

class BagList(APIView):
	"""
	API endpoint for managing bags.
	
	get:
	Return a list of all bags in the marketplace.
	
	post:
	Create a new bag listing (authentication required).
	"""
	permission_classes = (IsAuthenticatedOrReadOnly, )
	def get(self, request, format=None):			
		bags = Bag.objects.all()
		serializer = BagSerializer(bags, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = BagSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
	def perform_create(self, serializer):
		serializer.save(self.request.user)

class BagDetails(APIView):
	"""
	API endpoint for individual bag operations.
	
	get:
	Retrieve details of a specific bag.
	
	put:
	Update a bag listing (owner only).
	
	delete:
	Delete a bag listing (owner only).
	"""
	def get_object(self, pk):
		try:
			return Bag.objects.get(pk=pk)
		except Bag.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		bag = self.get_object(pk)
		serializer = BagSerializer(bag, context={'request': request})
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		bag = self.get_object(pk)
		serializer = BagSerializer(bag, data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		bag = self.get_object(pk)
		bag.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
	"""User management endpoint.
	
	get:
	Retrieve a list of all registered users.
	
	post:
	Register a new user account. Returns user details and authentication token.
	"""
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True, context={'request': request})
		return Response(serializer.data)
	
	@csrf_exempt
	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			user = serializer.save()
			if user:
				user_token = Token.objects.create(user=user)
				json_token = serializer.data
				json_token['token'] = user_token.key
				return Response(json_token, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
	"""Individual user operations.
	
	get:
	Retrieve details of a specific user.
	
	put:
	Update user information.
	
	delete:
	Delete a user account.
	"""
	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None, ):
		user = self.get_object(pk)
		serializer = UserSerializer(user, context={'request': request})
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserSerializer(user, data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		user = self.get_object(pk)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ShopList(APIView):
	"""Shop management endpoint.
	
	get:
	Retrieve a list of all shops in the marketplace.
	
	post:
	Create a new shop (authentication required).
	"""
	permission_classes = (IsAuthenticatedOrReadOnly,)
	#permission_classes =(IsOwnerOrReadOnly,)
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
	
	def get(self, request, format=None):
		shops = Shop.objects.all()
		serializer = ShopSerializer(shops, many=True,context={'request': request})
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = ShopSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		serializer.save(self.request.user)

class ShopDetail(APIView):
	"""Individual shop operations.
	
	get:
	Retrieve details of a specific shop.
	
	put:
	Update shop information (owner only).
	
	delete:
	Delete a shop (owner only).
	"""
	permission_classes =(IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,)
	def get_object(self, pk):
		try:
			return Shop.objects.get(pk=pk)
		except Shop.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None): 
		shop = self.get_object(pk)
		serializer = ShopSerializer(shop, context={'request': request})
		return Response(serializer.data)
	
	def put(self, request, pk, format=None):
		shop = self.get_object(pk)
		serializer = ShopSerializer(shop, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		shop = self.get_object(pk)
		shop.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileList(APIView):
	"""User profile management.
	
	get:
	Retrieve all user profiles.
	
	post:
	Create or update user profile information.
	"""
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def get(self, request, format=None):
		profile=Profile.objects.all()
		serializer=ProfileSerializer(profile, many=True,context={'request': request})
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = ProfileSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
	def perform_create(self, serializer):
		serializer.save(self.request.user)


class ProfileDetail(APIView):
	permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,)
	def get_object(self, pk):
		try:
			return Profile.objects.get(pk=pk)
		except Profile.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		profile = self.get_object(pk)
		serializer = ProfileSerializer(profile, context={'request': request})
		return Response(serializer.data)
	
	def put(self, request, pk, format=None):
		profile = self.get_object(pk)
		serializer  = ProfileSerializer(profile, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		profile = self.get_object(pk)
		serializer  = ProfileSerializer(request.user, data=request.data, context={'request': request}, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	
	def delete(self, request, pk, format=None):
		profile = self.get_object(pk)
		profile.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ContactList(APIView):
	"""Contact message management.
	
	get:
	Retrieve all contact messages.
	
	post:
	Submit a new contact message or inquiry.
	"""
	authentication_classes = (CsrfExceptSessionAuthentication,)
	def get(self, request, format=None):
		contacts = Contact.objects.all()
		serializer = ContactSerializer(contacts, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ContactSerializer(data=request.data,context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class AccountList(APIView):
	"""Financial account transactions.
	
	get:
	Retrieve all financial transactions.
	
	post:
	Create a new transaction (deposit or withdrawal).
	"""
	permission_classes = (IsAuthenticatedOrReadOnly, )
	def get(self, request, format=None):			
		accounts = Account.objects.all()
		serializer = AccountSerializer(accounts, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = AccountSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
	def perform_create(self, serializer):
		serializer.save(self.request.user)

class AccountDetails(APIView):
	"""Individual transaction operations.
	
	get:
	Retrieve details of a specific transaction.
	
	put:
	Update transaction details.
	
	delete:
	Delete a transaction record.
	"""
	def get_object(self, pk):
		try:
			return Account.objects.get(pk=pk)
		except Account.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		account = self.get_object(pk)
		serializer = AccountSerializer(account, context={'request': request})
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		account = self.get_object(pk)
		serializer = AccountSerializer(account, data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		account = self.get_object(pk)
		account.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ContactDetail(APIView):
	# permission_classes = (IsOwnerOrReadOnly, )	
	def get_object(self, pk):
		try:
			return Contact.objects.get(pk=pk)
		except Contact.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		contact = self.get_object(pk)
		serializer = ContactSerializer(contact,context={'request': request})
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		contact = self.get_object(pk)
		serializer = ContactSerializer(contact, data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		contact = self.get_object(pk)
		contact.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
	"""User authentication endpoint.
	
	post:
	Authenticate user with username and password.
	Returns authentication token on success.
	
	Request body:
	- username: User's username
	- password: User's password
	
	Response:
	- token: Authentication token for subsequent requests
	"""
	authentication_classes = (CsrfExceptSessionAuthentication, BasicAuthentication,)
	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		#user from the serializer's user = data['user']
		user_object = serializer.validated_data['user']
		login_to_django(request, user_object)
		#get user's token or create if not availabe	
		token, created =  Token.objects.get_or_create(user=user_object)	
		# request.META.get('WWW-Authentication', 'Token '+str(token))	
		return Response({'token':token.key},status=200)


class LogoutView(APIView):
	"""User logout endpoint.
	
	post:
	Log out the current user and invalidate their session.
	Requires authentication token.
	"""
	authentication_classes  = (TokenAuthentication, )
	@csrf_exempt
	def post(self, request):
		logout_to_django(request)
		return Response(status=204)
@api_view(['GET'])
def now_search(request):
	"""Search endpoint for bags, shops, and users.
	
	Query parameter:
	- q: Search query string
	
	Returns matching bags, shops, and users.
	"""
	query = request.GET.get("q")
	shops = Shop.objects.all()
	bags = Bag.objects.all()
	users = User.objects.all()
	print(query)
	if query:
		shops = shops.filter(name__icontains=query)
		bags = bags.filter(bags_type__icontains=query)
		users = users.filter(last_name__icontains = query)
	return JsonResponse({"shops":ShopSerializer(instance=shops, many=True,context={'request': request}).data,
						"bags":BagSerializer(instance=bags, many=True,context={'request': request}).data,
						"users":UserSerializer(instance=users, many=True,context={'request': request}).data,
	})



# class EverythingList(APIView):
# 	def get(self, resquest, format=None, **kwargs):
# 		bags = get_bag(request)
# 		bag_serializer = BagSerializer(bags)
# 		shop_serializer = ShopSerializer(shops)