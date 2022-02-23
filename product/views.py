from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from product.models import Product, Category
from product.mixin  import ProductMixinView
# Create your views here.

user_model = get_user_model()


class ProductListView(ListView):
    """Get All Product"""

    paginate_by: int = 5
    model: Product = Product
    template_name: str = "product.html"
    fields: list = [
        "id", 
        "name", 
        'selling_price', 
        'purchasing_price',
        'quantity', 
        "category", 
        'user'
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter by name proudct 
        queryset = queryset.filter(name__contains=self.request.GET.get("search", ''))
        # filter by categroy of product 
        if self.request.GET.get("category"):
            queryset = queryset.filter(category__name__contains=self.request.GET.get("category", ''))
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs: dict):
        # limit 
        self.paginate_by = self.request.GET.get("per_page", self.paginate_by)
        context = super().get_context_data(**kwargs)
        context['fields'] = self.fields # set field names in response 
        context['per_page'] = self.paginate_by # set per_page in response 
        context['categories'] = Category.objects.all() # set categories in response 
        return context
    

class ProductCreateView(ProductMixinView, CreateView) :
    """Create new product"""

    success_message = "Product %(name)s was created successfully"

    def form_valid(self, form):
        
        # set created by field  
        form.instance.user = self.request.user

        return super().form_valid(form)

    

class ProductUpdateView(ProductMixinView, UpdateView):
    """update product by id"""

    success_message = "Product %(name)s was updated successfully"


class ProductDeleteView(ProductMixinView, DeleteView):
    """Delete product by id"""

    success_message = "Product %(name)s was deleted successfully"
