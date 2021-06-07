from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, Account
from .forms import UserDepositForm, UserWithdrawForm, UserTransferForm
from decimal import *



def home(request):
    return render(request, 'automatedbankteller/home.html')

def about(request):
    return render(request, 'automatedbankteller/about.html')

@login_required
def transactions(request):
    context = {
        'transactions': Transaction.objects.filter(sender=request.user)
    }
    return render(request, 'automatedbankteller/transactions.html', context)

@login_required
def my_accounts(request):
    context = {
        'accounts': Account.objects.filter(account_owner=request.user)
    }
    return render(request, 'automatedbankteller/my_accounts.html', context)

@login_required
def deposit(request):
    if request.method == 'POST':
        form = UserDepositForm(request.POST)
        if form.is_valid():
            account_type = request.POST['account_type']
            if account_type == 'CA':
                account_type_one_or_two = 1
            else:
                account_type_one_or_two = 3

            amount = request.POST['amount']
            account = Account.objects.get(id=account_type_one_or_two)

            if Decimal(amount) > 0.0:
                account.deposit(amount)
                messages.success(request, f'$' + amount + ' has been deposited into your account!')
                return redirect('ABT-my_accounts')
            else:
                messages.warning(request, f'Please enter a deposit amount greater than 0.')
                return redirect('ABT-deposit')
    else:
        form = UserDepositForm(instance=request.user)

    return render(request, 'automatedbankteller/deposit.html', {'form': form})

@login_required
def withdraw(request):
    if request.method == 'POST':
        form = UserWithdrawForm(request.POST)
        if form.is_valid():
            account_type = request.POST['account_type']
            if account_type == 'CA':
                account_type_one_or_two = 1
            else:
                account_type_one_or_two = 3

            amount = request.POST['amount']
            account = Account.objects.get(id=account_type_one_or_two)

            if Decimal(amount) > account.account_amount:
                messages.warning(request, f'You cannot withdraw an amount greater than your current balance.')
                return redirect('ABT-my_accounts')
            elif Decimal(amount) > 10000:
                messages.warning(request, f'Please come in to our branch to make a withdraw of more than $10,000')
                return redirect('ABT-my_accounts')
            elif Decimal(amount) > 0.0:
                account.withdraw(amount)
                messages.success(request, f'$' + amount + ' has been withdrawn from your account!')
                return redirect('ABT-my_accounts')
            else:
                messages.warning(request, f'Please enter a withdraw amount greater than 0.')
                return redirect('ABT-withdraw')
    else:
        form = UserWithdrawForm(instance=request.user)

    return render(request, 'automatedbankteller/withdraw.html', {'form': form})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = UserTransferForm(request.POST)
        if form.is_valid():
            #form.save()
            accountID_sender = request.POST['accountID_sent']
            accountID_receiver = request.POST['accountID_received']
            transfer_amount = request.POST['amount']
            print(accountID_sender)
            print(accountID_receiver)
            print(request.user)
            print(transfer_amount)

            owner = Account.objects.get(accountID=accountID_sender)
            user_receiving = Account.objects.get(accountID=accountID_receiver)
            fees_account = Account.objects.get(pk=5)
            print(owner.pk)
            print(owner)
            print(user_receiving.pk)
            print(user_receiving)


            if str(owner) == str(request.user):
                if Decimal(transfer_amount) > owner.account_amount:
                    messages.warning(request, f'You do not have sufficient funds in this account.')
                    return redirect('ABT-my_accounts')
                elif Decimal(transfer_amount) > 10000:
                    messages.warning(request, f'Please come in to our branch to make a transfer more than $10,000')
                    return redirect('ABT-my_accounts')
                elif Decimal(transfer_amount) > 0.0:
                    print(owner.account_amount)
                    owner.account_send_logic(transfer_amount)
                    print(owner.account_amount)
                    print(transfer_amount)
                    user_receiving.account_receive_logic(transfer_amount)
                    fees_account.fee_structure()
                    messages.success(request, f'Transfer Complete.')
                    return redirect('ABT-my_accounts')
                else:
                    messages.warning(request, f'You must enter a transfer amount greater than $0.')
                    return redirect('ABT-my_accounts')
            else:
                messages.warning(request, f'You do not own this account. Please check that you entered the correct account information.')
                return redirect('ABT-transfer')

            #sender, seijih checking = 6532013431
                    #seijih savings = 4520013697
            #reciver = 3240958618
        else:
            messages.warning(request, f'Form is not Valid.')
            return redirect('ABT-my_accounts')

    else:
        form = UserTransferForm()

    context = {
        'accounts': Account.objects.filter(account_owner=request.user),
        'form': form
    }
    return render(request, 'automatedbankteller/transfer.html', context)
