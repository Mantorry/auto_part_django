from django.urls import path
from . import views

app_name = 'receipt'

urlpatterns = [
    path('', views.receipt_list, name='receipt_list'),
    path('create/', views.receipt_create, name='receipt_create'),
    path('<int:pk>/', views.receipt_detail, name='receipt_detail'),
    path('<int:pk>/confirm/', views.receipt_confirm, name='receipt_confirm'),
    path('<int:pk>/export/', views.receipt_export, name='receipt_export'),
    path('supplies/', views.supply_list, name='supply_list'),
    path('supplies/<int:pk>/', views.supply_detail, name='supply_detail'),
]
