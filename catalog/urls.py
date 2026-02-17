from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='search'),
]

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='search'),
]
