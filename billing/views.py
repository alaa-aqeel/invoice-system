from django.db.models import Sum
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
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
    """Create billing"""
    model = Bill 
    template_name: str = "forms/billing_form.html"
    fields: list = [
        'code',
        'note',
        "discount",
        "account",
    ]

    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.object.pk])

    def form_valid(self, form):
        
        # set created by field  
        form.instance.user = self.request.user
        return super().form_valid(form)

class BillingUpdateView(UpdateView):
    """Create billing"""

    model = Bill 
    template_name: str = "forms/billing_form.html"
    fields: list = [
        'code',
        'note',
        "discount",
        "account",
    ]

    def get_success_url(self) -> str:
        return reverse("billing")

    def get_products(self):
        return Product.objects.all()

    def get_billing_products(self):
        bills = BillProducts.objects.filter(bill__id=self.kwargs.get("pk"))
        return bills

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.get_products()
        context['fields'] = [
            "id",
            'product',
            'quantity',
            'price',
        ]
        context["bill_products"] = self.get_billing_products()
        context["total_price"] = self.get_billing_products().aggregate(Sum('price')).get("price__sum", 0)
        return context

    def form_valid(self, form):
        form.instance.total_price = self.get_billing_products().aggregate(Sum('price')).get("price__sum", 0)
        return super().form_valid(form)

class BillDeleteView(DeleteView):
    model = Bill 

    def get_success_url(self) -> str:
        return reverse("billing")   

class BillProductCreateView(CreateView):

    model = BillProducts 
    template_name: str = "forms/billing_products_form.html"
    fields: list = [
        # 'price',
        'quantity',
        'product',
        'note',
    ]


    def get_success_url(self) -> str:

        return reverse("billing_update", args=[self.kwargs.get("billId")])

    def form_valid(self, form):
        
        # set price of product
        form.instance.price =  form.instance.product.price * form.instance.quantity

        # set billing 
        form.instance.bill = Bill.objects.get(pk=int(self.kwargs.get("billId")))
        return super().form_valid(form)


class BillProductUpdateView(UpdateView):

    model = BillProducts 
    template_name: str = "forms/billing_products_form.html"
    fields: list = [
        # 'price',
        'quantity',
        'product',
        'note',
    ]


    def get_success_url(self) -> str:

        return reverse("billing_update", args=[self.kwargs.get("billId")])

    def form_valid(self, form):
        
        # set price of product
        form.instance.price =  form.instance.product.price * form.instance.quantity
        return super().form_valid(form)

class BillProductDeleteView(DeleteView):

    model = BillProducts 

    def get_success_url(self) -> str:

        return reverse("billing_update", args=[self.kwargs.get("billId")])