from django.urls import path
from billing.views import BillingListView, BillingCreateView, BillDeleteView, BillingUpdateView, BillProductCreateView, BillProductDeleteView, BillProductUpdateView

urlpatterns = [

    path("", BillingListView.as_view(), name="billing"),
    path("create", BillingCreateView.as_view(), name="billing_create"),
    path("update/<pk>", BillingUpdateView.as_view(), name="billing_update"),
    path("delete/<pk>", BillDeleteView.as_view(), name="billing_delete"),
    path("<billId>/product/", BillProductCreateView.as_view(), name="billing_products_create"),
    path("<billId>/product/<pk>/update", BillProductUpdateView.as_view(), name="billing_products_update"),
    path("<billId>/product/<pk>/delete", BillProductDeleteView.as_view(), name="billing_products_delete"),
]

