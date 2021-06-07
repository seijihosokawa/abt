from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Transaction, Account

#deposit function
@receiver(post_save, sender=User)
def deposit(amount):
    instance = float(amount)
    Account.account_amount += instance
