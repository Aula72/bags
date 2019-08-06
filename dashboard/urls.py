from django.urls import path
from dashboard import views
app_name="dashboard"
urlpatterns = [
	path('', views.index, name='index'),
	path('contact/', views.contact, name='contact'),
	path('shops/', views.shops, name='shops'),
	path('create-shop/', views.create_shop, name='create-shop'),
	path("shops/<str:pk>/",views.shopdetails,name='shop-details'),
	path('bags/', views.bags, name="bags"),
	path('create-bag/', views.create_bag, name='create-bag'),
	path('bags/<str:pk>/', views.bagdetails, name="bag-details"),
	path('accounts/', views.accounts, name='accounts'),
	path('create-account/', views.create_account, name='create-account'),
	path('accounts/<str:pk>/', views.accountdetails, name="account-details"),
	path('accounts/', views.accounts, name='accounts'),
	path('logout/', views.logout, name='logout'),
	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('profile-update/', views.profile, name='profile'),
]