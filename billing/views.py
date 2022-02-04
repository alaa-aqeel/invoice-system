from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from billing.models import Bill, BillProducts
from product.models import Product
# Create your views here.




class BillingListView(ListView):
    
    paginate_by: int = 5
    model: Bill = Bill
    template_name: str = "billing.html"
    fields: list = [
        "id", 
        'code',
        'price',
        "discount",
        "created_at",
        "account",
        "user"
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fields"] = self.fields 

        return context



class BillingCreateView(CreateView):

    
    # model base-view 
    model = Bill

    # successfuly redirect  
    success_url = reverse_lazy("product")

    # template form 
    template_name: str = "forms/billing_form.html"

    # form fields 
    fields: list = [
        'code',
        'note',
        "discount",
        "account",
    ]

    def get_products(self, request):
        products = Product.objects.all()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_products(self.request)
        return context