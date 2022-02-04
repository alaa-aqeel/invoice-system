from django.urls import path
from product.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView


urlpatterns = [

    path("", ProductListView.as_view(), name="product"),
    path("create", ProductCreateView.as_view(), name="product_create"),
    path("update/<pk>", ProductUpdateView.as_view(), name="product_update"),
    path("delete/<pk>", ProductDeleteView.as_view(), name="product_delete"),
]
