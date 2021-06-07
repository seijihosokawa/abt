from django import forms
from .models import Account, Transaction


class UserDepositForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = Account
        fields = ['account_type', 'amount']
        labels = {
            'account_type': 'Account Type',
        }


class UserWithdrawForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = Account
        fields = ['account_type', 'amount']
        labels = {
            'account_type': 'Account Type',
        }

class UserTransferForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'accountID_sent', 'description', 'accountID_received']
        labels = {
            'accountID_sent': 'Account ID Sending',
            'accountID_received': 'Account ID Receiving',
        }