from django.contrib import admin
from .models import  Bag, Shop, Profile,Contact, Account

# from django.contrib.auth.models import User
# Register your models here.
# admin.site.register(User)
class BagAdmin(admin.ModelAdmin):
	fields = ('owner', 'shop','price', 'bag_type','bag_size', 
			'buying_type', 'payment_type', 'image_one',  'image_two', 
			'image_three', 'image_four', 'simple_description', )
	list_display = ['id','owner', 'shop','price', 'bag_type','bag_size', 
			'buying_type', 'payment_type', 'image_one',  'image_two', 
			'image_three', 'image_four', 'simple_description']
	class Meta:
		model = Bag

class ShopAdmin(admin.ModelAdmin):
	fields = ('name', 'description', 'owner', 'location', 'contact', 'email')
	list_display = ['id','name', 'description', 'owner', 'location', 'contact', 'email']
	class Meta:
		model = Shop

class ProfileAdmin(admin.ModelAdmin):
	fields =  ('owner', 'phone', 'gender', 'photo', 'User_type', 'nin')
	list_display = ['id', 'owner', 'phone', 'gender', 'photo', 'User_type', 'nin']
	class Meta:
		model = Profile

class ContactAdmin(admin.ModelAdmin):
	fields = ('name', 'email', 'subject','message')
	list_display = ['id', 'name', 'email', 'subject', 'message']
	class Meta:
		model = Contact

class AccountAdmin(admin.ModelAdmin):
	fields = ('owner', 'trans_type', 'amount')
	list_display = ['id','owner', 'trans_type', 'amount']
	class Meta:
		model = Account
admin.site.register(Bag, BagAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Account, AccountAdmin)
