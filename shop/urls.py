from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('api/brands/', views.brands_list, name='brands-list'),
    path('api/categories/', views.categories_list, name='categories-list'),
    path('api/products/', views.products_list, name='products-list'),
    path('products/', views.products_page, name='products-page'),
]
