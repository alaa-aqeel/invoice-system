from django.db.models import Q
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.db.models import Sum
from datetime import datetime
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from billing.models import Bill, BillProducts
from product.models import Product
from billing.utils import generate_billing_number
# Create your views here.


class BillingListView(ListView):
    """Billing View Page"""
    # limit page 
    paginate_by: int = 5
    model: Bill = Bill
    template_name: str = "billing.html"

    # Datatable column names
    fields: list = [
        "id", 
        'number',
        'price',
        "discount",
        "account",
        "user",
        "canceled_date",
        "created_date",
    ]

    def get_queryset(self) :
        search = self.request.GET.get("search", "")
        date_start = self.request.GET.get("date_start", None)
        date_end = self.request.GET.get("date_end", None)
        
        queryset = super().get_queryset().order_by('id')
        # filter by account name or user username 
        queryset = queryset.filter(
            Q(account__fullname__contains=search) 
            | Q(number__contains=search) 
            | Q(user__username__contains=search)
        )
        if date_start:
            # Filter by created_at when Greater than `date_start`
            queryset = queryset.filter(created_at__gte=date_start)
        if date_end:
            # Filter by created_at when less than `date_end`
            queryset = queryset.filter(created_at__lt=date_end)
        return queryset

    def get_context_data(self, **kwargs):
        # limit 
        self.paginate_by = self.request.GET.get("per_page", self.paginate_by)
        context = super().get_context_data(**kwargs)
        context["fields"] = self.fields # set fields for datatable
        context['per_page'] = self.paginate_by # set per_page in response 
        return context

class BillingCreateView(CreateView):
    """Create Billing"""

    model = Bill 
    template_name: str = "forms/billing_form.html"
    fields: list = [
        'number',
        'note',
        "discount",
        "account",
    ]

    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.object.pk])

    def get_form(self):
        form = super().get_form()
        form.fields["number"].initial = generate_billing_number()
        return form

    def form_valid(self, form):

        # set user created by 
        form.instance.user = self.request.user
        return super().form_valid(form)

class BillingUpdateView(UpdateView):
    """Update billing by id"""

    model = Bill 
    template_name: str = "forms/billing_form.html"
    fields: list = [
        'number',
        'note',
        "discount",
        "account",
    ]

    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.kwargs.get("pk")])

    def get_products(self):
        return Product.objects.all()

    def get_billing_products(self):
        bills = BillProducts.objects.filter(bill__id=self.kwargs.get("pk"))
        return bills


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fields for datatable `bill_products`
        context['fields'] = [
            "id",
            'product',
            'quantity',
            'price',
        ]
        billing_products = self.get_billing_products()
        context["bill_products"] = billing_products
        context["billing"] = self.get_object()
        context["total_price_of_products"]  = billing_products.aggregate(Sum('price')).get("price__sum", 0) 
        return context

    def form_valid(self, form):
        form.instance.total_price = self.get_billing_products().aggregate(Sum('price')).get("price__sum", 0) - int(form.instance.discount)
        return super().form_valid(form)

class BillDeleteView(DeleteView):
    model = Bill 

    def get_success_url(self) -> str:
        return reverse("billing")   


    def update_quantity_product(self):
        current_billing = self.get_object()
        for billing_product in current_billing.bill_products.all():
            product = billing_product.product 
            product.quantity = product.quantity + billing_product.quantity 
            product.save()

    def dispatch(self, request, *args, **kwargs):
        current_object = self.get_object()
        self.update_quantity_product()
        current_object.deleted_at = datetime.now()
        current_object.save()
        return HttpResponseRedirect(self.get_success_url())
        



class BillProductCreateView(CreateView):

    model = BillProducts 
    template_name: str = "forms/billing_products_form.html"
    fields: list = [
        'quantity',
        'product',
        'note',
    ]


    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.kwargs.get("billId")])

    def get_price_product(self, form):
        """Get price of product (Selling price * quantity)"""
        return form.instance.product.selling_price * form.instance.quantity

    def update_quantity_product(self, form):
        product = form.instance.product
        quantity = product.quantity - form.instance.quantity
        if quantity < 0:
            return product.quantity
        product.quantity = quantity
        product.save()

    def get_products(self):
        return Product.objects.all()

    def get_current_billing(self):
        return Bill.objects.get(pk=int(self.kwargs.get("billId")))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.get_products() 
        return context
    
    def form_valid(self, form):
        # set price of product
        form.instance.price =  self.get_price_product(form)
        # set billing 
        form.instance.bill = self.get_current_billing()
        is_not_none = self.update_quantity_product(form)
        if is_not_none != None:
            form.errors.update({
                "quantity": [u"You have %s of the product"%is_not_none]
            })
            return super().form_invalid(form)
        return super().form_valid(form)

class BillProductUpdateView(UpdateView):

    model = BillProducts 
    template_name: str = "forms/billing_products_form.html"
    fields: list = [
        'quantity',
        'product',
        'note',
    ]


    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.kwargs.get("billId")])

    def get_price_product(self, form):
        """Get price of product (Selling price * quantity)"""
        return form.instance.product.selling_price * form.instance.quantity

    def calculating_quantity(self, form):
        """Calculating quantity for product"""
        current_billing_product = self.get_object()
        product_quantity = form.instance.product.quantity
        calculating_result = current_billing_product.quantity - form.instance.quantity
        return product_quantity + calculating_result


    def update_quantity_product(self, form):
        product = form.instance.product
        product.quantity = self.calculating_quantity(form)
        if product.quantity < 0:
            return product.quantity
        product.save()

    def form_valid(self, form):
        # set price of product
        form.instance.price =  self.get_price_product(form)
        if self.update_quantity_product(form):
            form.errors.update({
                "quantity": [u"Quantity is out of stock"]
            })
            return super().form_invalid(form)
        return super().form_valid(form)

class BillProductDeleteView(DeleteView):

    model = BillProducts 

    def get_success_url(self) -> str:
        return reverse("billing_update", args=[self.kwargs.get("billId")])

    def update_quantity_product(self):
        current_billing_product = self.get_object()
        product = current_billing_product.product 
        product.quantity = product.quantity + current_billing_product.quantity 
        product.save()

    def dispatch(self, request, *args, **kwargs):
        self.update_quantity_product()
        return super().dispatch(request, *args, **kwargs)
    