from django.urls import path
from .views import *


urlpatterns = [
    #path('', views.index, name='index'),

    #Leave as empty string for base url
	path('', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),


    path('showproducts/', product_info_sql, name='showproducts'),
    path('home/', home_view, name='home'),
    path('product/<str:product_id>/', product_view, name='product'),
]