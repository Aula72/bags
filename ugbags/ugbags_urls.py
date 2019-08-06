from django.urls import path, include
# from django.conf.urls import url
from ugbags import ugbags_views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'ugbags'

urlpatterns = [
	path('', ugbags_views.api_root),
	path('bags/', ugbags_views.BagList.as_view(), name='bag-lists' ),
	path('bags/<uuid:pk>/', ugbags_views.BagDetails.as_view(), name='bag-details'),
	path('users/', ugbags_views.UserList.as_view(), name='user-list'),
	path('users/<int:pk>/', ugbags_views.UserDetail.as_view(), name='user-details'),
	path('shops/', ugbags_views.ShopList.as_view(), name='shop-list'),
	path('shops/<uuid:pk>/', ugbags_views.ShopDetail.as_view(), name='shop-detail'),
	path('register/', ugbags_views.UserList.as_view(), name='account-create'),
	path('profiles/', ugbags_views.ProfileList.as_view(), name='profile-list'),
	path('profiles/<uuid:pk>/', ugbags_views.ProfileDetail.as_view(), name='profile-details'),
	path('financial-accounts/', ugbags_views.AccountList.as_view(), name='account-list'),
	path('financial-accounts/<uuid:pk>/', ugbags_views.AccountDetails.as_view(), name='account-details'),
	path('contact/',ugbags_views.ContactList.as_view(), name='contact-list'),
    path('contact/<uuid:pk>/', ugbags_views.ContactDetail.as_view(), name='contact-details'),
	path('search/', ugbags_views.now_search, name='search-results'),
    path('login/', ugbags_views.LoginView.as_view(), name='login'),
    path('logout/', ugbags_views.LogoutView.as_view(), name='logout'),
	# path('rest-auth/', include('rest_auth.urls'), name='login'),
	# path('rest-auth/register/', include('rest_auth.registration.urls'), name='register'),
	# path('logout/', include(), name='logout'),
	
	# url(r'^users/resources/profile_pics/[Aa-zZ0-9]+$', name='profile-image'),
]

