from django.shortcuts import render
from django.views.generic import ListView
from product.models import Product
# Create your views here.


class ProductListView(ListView):
    """Get All Product"""

    paginate_by = 2
    # context_object_name = "products"
    model = Product
    template_name = "product.html"
    fields = [
        "id", 
        "name", 
        'price', 
        'quantity', 
        "category", 
        'user'
    ]

    def get_context_data(self, **kwargs):

        # set records per page 
        self.paginate_by = self.request.GET.get("per_page", self.paginate_by)

        context = super().get_context_data(**kwargs)

        # get all column names 
        context['fields'] = self.fields
        context['per_page'] = self.paginate_by
        
        return context
    