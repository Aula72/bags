from rest_framework import serializers, exceptions
from ugbags.models import  Bag, Shop, Profile, Contact, Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		username = data.get("username", "")
		password = data.get('password', '')

		if username and password:
			user_object = authenticate(username=username, password=password)
			if user_object:
				if user_object.is_active:
					data['user'] = user_object
				else:
					message = 'Account not yet activated, please activated your account!'
					raise exceptions.ValidationError(message)
			else:
				message = 'Username or Password is wrong, Please try again!'
				raise exceptions.ValidationError(message)
		else:
			message = 'Both Username and Password are required!'
			raise exceptions.ValidationError(message)
		return data
class UserSerializer(serializers.ModelSerializer):	
	bag = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='ugbags:bag-details', 
		)
	
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(min_length=8, required=True, write_only=True)
	def create(self, validated_data):
		user = User.objects.create_user(validated_data['username'], validated_data['email'],  validated_data['password'])
		return user
	class Meta:
		model = User
		fields = ('id','email', 'username', 
			 'bag', 'password',)
	def get_photo_url(self, obj):
		request = self.context.get('request')
		photo = obj.photo.image
		return request.build_absolute_url(photo.url)

		
class BagSerializer(serializers.ModelSerializer):
	buying_type = serializers.CharField(source='get_buying_type_display')
	bag_size = serializers.CharField(source='get_bag_size_display')
	bag_type = serializers.CharField(source='get_bag_type_display')
	payment_type = serializers.CharField(source='get_payment_type_display')

	owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
	url = serializers.HyperlinkedIdentityField(view_name="ugbags:bag-details", read_only=True)
	id = serializers.CharField(read_only=True)
	class Meta:
		model = Bag
		fields = ('id', 'owner', 'price', 'bag_type','bag_size', 
			'buying_type', 'payment_type', 'image_one',  'image_two', 
			'image_three', 'image_four', 'simple_description', 'url' )

	
class ShopSerializer(serializers.ModelSerializer):
	bag = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='ugbags:bag-details', 
		)
	# bag = BagSerializer()
	# owner = serializers.ReadOnlyField(source='owner.username')
	url = serializers.HyperlinkedIdentityField(view_name="ugbags:shop-detail")
	owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
	# id = serializers.CharField(read_only=True)
	class Meta:
		model = Shop
		fields = ("id",'name', 'description', 'owner', 'location', 'contact', 'email', 'bag', 'url')
		extra_kwargs = {
			'owner':{
				'read_only':True, 
				'required':False,
				'default':serializers.CurrentUserDefault()
			}
		}
class AccountSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
	url = serializers.HyperlinkedIdentityField(view_name='ugbags:account-details')
	trans_type = serializers.CharField(source='get_trans_type_display')
	class Meta:
		model = Account
		fields = ('id', 'owner', 'trans_type', 'amount','url')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	user_type = serializers.CharField(source='get_User_type_display')
	gender = serializers.CharField(source='get_gender_display')
	owner = serializers.ReadOnlyField(source='owner.username')
	url = serializers.HyperlinkedIdentityField(view_name='ugbags:profile-details')
	class Meta:
		model = Profile
		fields = ( 'id', 'owner', 'phone', 'gender', 'photo', 'user_type', 'nin','url')

class ContactSerializer(serializers.HyperlinkedModelSerializer):	
	url = serializers.HyperlinkedIdentityField(view_name='ugbags:contact-details', read_only=True)
	id = serializers.CharField(read_only=True)
	class Meta:
		model = Contact
		fields = ('id', 'email','name', 'subject','message', 'url')

class EverythingSerializer(serializers.ModelSerializer):
	users = UserSerializer(many=True)
	shops = ShopSerializer(many=True)
	bags  = BagSerializer(many=True)
	profiles = ProfileSerializer(many=True) 