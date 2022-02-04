from django.urls import path
from billing.views import BillingListView, BillingCreateView

urlpatterns = [

    path("", BillingListView.as_view(), name="billing"),
    path("create", BillingCreateView.as_view(), name="billing_create"),
]

