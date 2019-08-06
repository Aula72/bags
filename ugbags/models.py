from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from regex_field.fields import RegexField
from django.contrib.auth.models import User
from .get_username import get_current_user
import uuid
# from django.contrib.auth.models import AbstractUser
# Create your models here.
GENGER = (('m','male'), ('f','female'))
TYPES = (('b','buyer'),('s','seller'), ('a','admin'))
BAGTYPE = (('a', 'office'), 
			('b', 'laptop'), 
			('c', 'lady_hand_bag'), 
			('d','school'),
			('e','travel'), 
			('f',"men's wallet"), 
			('g',"women's wallet"))
BAGSIZE = (('a','small'), 
			('b', 'big'), 
			('c', 'medium'), 
			('d','large'),
			('e','extra-large'), 
			('f','extra-small'))
SKINTYPE = (('a','lether'), ('b','cloth'))
COLOR = (
	('a','white'),('b','black'),
	('c','red'),('c','blue'),
	('d','purple'),	('e','green'),
	('f','yellow'),('g','grey'),
	('h','pink'),('i','other'),
	('j','not specific')
	)
PRICETYPE = (('a','not negotiable'),('b', 'slightly negotiable'), ('c', 'negotiable'))
BUYTYPE = (('a','pay via app'), ('b', 'pay cash on delievery'))
REPORT = (
	('a', 'abusive'), 
	('b', 'ill-described'), 
	('c', 'over-priced'), 
	('d','not available in shop'), 
	('e','harrassed'), 
	('f', 'shop does not exist'), 
	('g', 'not delivered')
	)
TRANSACT = (('a','deposit'), ('b', 'withdraw'),)


class Profile(models.Model):
	id = models.UUIDField(unique=True, primary_key=True)
	owner = models.ForeignKey(User, related_name='profile', default=get_current_user,on_delete=models.CASCADE)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	gender = models.CharField(max_length = 1, choices=GENGER)
	photo = models.ImageField(upload_to='resources/profile_pics/')
	User_type = models.CharField(max_length=1, choices=TYPES)
	nin = models.CharField(max_length=14)
	update_by = models.ForeignKey(User,  related_name="+",default=get_current_user,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.phone)+'---'+self.gender+'---'+self.User_type
	def save(self, *args, **kwargs):
		user =  get_current_user()
		if not self.pk:
			self.owner = user
			self.id = uuid.uuid4()
		else:
			self.update_by = user
		super(Profile, self).save(*args, **kwargs)
class Shop(models.Model):
	id = models.UUIDField(unique=True, primary_key=True)
	name = models.CharField(max_length=200)
	description = models.TextField()
	owner = models.ForeignKey(User, related_name='shops', on_delete=models.CASCADE)
	location = models.CharField(max_length=900)
	contact = PhoneNumberField(null=False, blank=False, unique=True)
	email = models.EmailField(null=False, blank=False, unique=True)
	update_by = models.ForeignKey(User, related_name="+", default=get_current_user,on_delete=models.CASCADE)
	
	def save(self, *args, **kwargs):
		user =  get_current_user()
		if not self.pk:
			self.owner = user
			self.id = uuid.uuid4()
		else:
			self.update_by = user
		super(Shop, self).save(*args, **kwargs)
	def __str__(self):
		return self.name

class Bag(models.Model):
	id = models.UUIDField(unique=True, primary_key=True)
	owner = models.ForeignKey(User, related_name='bag', on_delete=models.CASCADE)
	shop = models.ForeignKey(Shop, related_name='bag', on_delete=models.CASCADE)
	# highlighted = models.TextField()
	price = models.IntegerField()
	bag_type = models.CharField(max_length=1, choices=BAGTYPE)
	bag_size = models.CharField(max_length=1, choices=BAGSIZE)
	skin_type = models.CharField(max_length=1, choices=SKINTYPE)
	bag_color = models.CharField(max_length=1, choices=COLOR)
	buying_type = models.CharField(max_length=1, choices=PRICETYPE)
	payment_type = models.CharField(max_length=1, choices=BUYTYPE)
	image_one = models.ImageField(upload_to='resources/bag_image/one')
	image_two = models.ImageField(upload_to='resources/bag_image/two', null=True, blank=True)
	image_three = models.ImageField(upload_to='resources/bag_image/three', null=True, blank=True)
	image_four = models.ImageField(upload_to='resources/bag_image/four', null=True, blank=True)
	update_by = models.ForeignKey(User, related_name="+", default=get_current_user,on_delete=models.CASCADE)
	simple_description = models.TextField()
	class Meta:
		unique_together=('id',)
		ordering = ['id']
	def __str__(self):
		return str(self.price)+'--'+self.bag_type+'---'+self.bag_color
	def save(self, *args, **kwargs):
		user =  get_current_user()
		if not self.pk:
			self.owner = user
			self.id = uuid.uuid4()
		else:
			self.update_by = user
		super(Bag, self).save(*args, **kwargs)
class Account(models.Model):
	id = models.UUIDField(unique=True, primary_key=True)
	owner = models.ForeignKey(User, related_name='account', on_delete=models.CASCADE)
	trans_type = models.CharField(max_length=1,verbose_name='Transaction Type', choices=TRANSACT)
	amount = models.IntegerField()
	def save(self, *args, **kwargs):
		user =  get_current_user()
		if self.trans_type == 'b':
			self.amount = -1*self.amount
		if self.trans_type=='a' and self.amount<0:
			self.amount = -1*self.amount
		if not self.pk:
			self.owner = user
			self.id = uuid.uuid4()
		else:
			self.update_by = user
		super(Account, self).save(*args, **kwargs)
class Contact(models.Model):
	id = models.UUIDField(unique=True, primary_key=True)
	email = models.EmailField()
	name = models.CharField(max_length=200, blank=True, null=True)
	subject = models.CharField(max_length=200, blank=True, null=True)
	message =  models.TextField()
	def save(self, *args, **kwargs):
		self.id = uuid.uuid4()
		super(Contact, self).save(*args, **kwargs)
class ReportShop(models.Model):
	pass

class ReportBag(models.Model):
	pass

class ReportUser(models.Model):
	pass
	
class RateShop(models.Model):
	pass

class RateSeller(models.Model):
	pass

class RateBag(models.Model):
	pass
