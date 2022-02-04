from django.urls import path
from account.views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView


urlpatterns = [
    path("", AccountListView.as_view(), name="account"),
    path("create", AccountCreateView.as_view(), name="account_create"),
    path("update/<pk>", AccountUpdateView.as_view(), name="account_update"),
    path("delete/<pk>", AccountDeleteView.as_view(), name="account_delete"),
]
