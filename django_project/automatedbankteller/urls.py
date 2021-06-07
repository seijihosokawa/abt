from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ABT-home'),
    path('about/', views.about, name='ABT-about'),
    path('my_accounts/', views.my_accounts, name='ABT-my_accounts'),
    path('account_history/', views.transactions, name='ABT-transactions'),
    path('deposit/', views.deposit, name='ABT-deposit'),
    path('withdraw/', views.withdraw, name='ABT-withdraw'),
    path('transfer/', views.transfer, name='ABT-transfer'),
]
