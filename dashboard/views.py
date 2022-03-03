from datetime import datetime
from django.shortcuts import render
from django.db.models import Count, Sum
from billing.models import Bill, BillProducts
from product.models import Product
from account.models import Account, Type
from debts.models import Debt
# Create your views here.

def not_found_page(request, exception):
    return render(request, "errors/404.html", status=404)

def index(request):
    billing = Bill.objects.values('created_at__month', 'created_at__year').annotate(count=Count('id'))
    accounts_type = Account.objects.values('type__name').annotate(count=Count('id'))
    accounts = sorted(Account.objects.all(), key=lambda account: account.balance, reverse=True)

    return render(request, "index.html", {
        "fields_accounts": ["id", "fullname", "balance"],
        "fields_accounts_type": ["type__name", "count"],
        "billing": billing,
        "accounts_type": accounts_type,
        "accounts": accounts,
    })