from django.db import models
from django.contrib.auth.models import User
from decimal import *


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    accountID_sent = models.IntegerField()
    accountID_received = models.IntegerField()

    def __str__(self):
        return str(self.amount)


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('SA', 'Savings'),
        ('CA', 'Checking'),
    )
    accountID = models.IntegerField()
    account_amount = models.DecimalField(max_digits=20, decimal_places=2)
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
    account_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.accountID)

    def get_balance(self):
        return self.account_amount

    def deposit(self, amount):
        self.account_amount = self.account_amount + Decimal(amount)
        self.save()
        return

    def withdraw(self, amount):
        self.account_amount = self.account_amount - Decimal(amount)
        self.save()
        return

    def fee_structure(self):
        self.account_amount = self.account_amount + 30
        self.save()
        return

    def account_send_logic(self, transfer_amount):
        self.account_amount = self.account_amount - (Decimal(transfer_amount) + 15)
        self.save()
        return

    def account_receive_logic(self, transfer_amount):
        self.account_amount = self.account_amount + (Decimal(transfer_amount) - 15)
        self.save()
        return