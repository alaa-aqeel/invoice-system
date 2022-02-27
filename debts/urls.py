from django.urls import path
from debts.views import DebtsListView, DebtsCreateView, DebtsUpdateView, DebtsDeleteView

urlpatterns = [
    
    path("", DebtsListView.as_view(), name="debts"),
    path("create", DebtsCreateView.as_view(), name="debts_create"),
    path("update/<pk>", DebtsUpdateView.as_view(), name="debts_update"),
    path("delete/<pk>", DebtsDeleteView.as_view(), name="debts_delete"),
]

