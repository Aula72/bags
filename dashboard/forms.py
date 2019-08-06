from django import forms
from django.utils.translation import ugettext_lazy as _
GENGER = (('m','male'), ('f','female'))
TYPES = (('b','buyer'),('s','seller'), ('a','admin'))
BAGTYPE = (('a', 'office'), ('b', 'laptop'), ('c', 'lady_hand_bag'), ('d','school'),('e','travel'), ('f',"men's wallet"), ('g',"women's wallet"))
BAGSIZE = (('a','small'), ('b', 'big'), ('c', 'medium'), ('d','large'),('e','extra-large'), ('f','extra-small'))
SKINTYPE = (('a','lether'), ('b','cloth'))
COLOR = (
    ('a','white'),('b','black'),
    ('c','red'),('c','blue'),
    ('d','purple'), ('e','green'),
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

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        
        'placeholder':'Your Name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        
        'placeholder':'Your Email Address'
    }))
    subject = forms.CharField(max_length=200,empty_value=True, widget=forms.TextInput(attrs={
        
        'placeholder':'Enter Subject Here'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'cols':80, 
        'rows':20, 
        
        'placeholder':'Your message'
    }))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    passwords = forms.CharField(max_length=100, widget=forms.PasswordInput()) 

class AccountForm(forms.Form):
    transaction_type = forms.ChoiceField(choices=TRANSACT)
    amount = forms.IntegerField()

class ProfileForm(forms.Form):
    phone_number = forms.CharField(max_length=14)
    gender = forms.ChoiceField(choices=GENGER)
    photo = forms.ImageField()   
    user_type = forms.ChoiceField(choices=TYPES) 
    nin = forms.CharField(max_length=14)

class ShopForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea())    
    location = forms.CharField(max_length=900)
    contact = forms.CharField(max_length=12)
    email = forms.EmailField()

class BagForm(forms.Form):
    price = forms.IntegerField(label="Price")
    bag_type = forms.ChoiceField(choices=BAGTYPE, label="Type")
    bag_size = forms.ChoiceField(choices=BAGSIZE, label="Size")
    skin_type = forms.ChoiceField(choices=SKINTYPE, label="Skin Type")
    bag_color = forms.ChoiceField(choices=COLOR, label="Color")
    buying_type = forms.ChoiceField(choices=PRICETYPE, label="Buying Type")
    payment_type = forms.ChoiceField(choices=BUYTYPE, label="Payment Type")
    image_one = forms.ImageField(label="Upload bag's Image(s)")
    image_two = forms.ImageField(label="Second Image(If Any)")
    image_three = forms.ImageField(label="Third Image(If Any)")
    image_four = forms.ImageField(label="Forth Image(If Any)")
    simple_description = forms.CharField(widget=forms.Textarea(), label="Description")

class RegisterForm(forms.Form):
    email = forms.EmailField(label="Your Email Address")
    username = forms.CharField(max_length=50, label="Your Username")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label="Your Password") 

    # fields = ('email', 'username', 'password')

    # labels =   {
    #     'email':_("Email Me"),
    # }  
