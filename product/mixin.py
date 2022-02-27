from product.models import Product
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class ProductMixinView(SuccessMessageMixin):

    model: Product = Product
    success_url = reverse_lazy("product")
    success_message = "Product %(name)s was successfully"
    template_name: str = "forms/porduct_form.html"
    fields: list = [
        "name", 
        'purchasing_price', 
        'selling_price', 
        'quantity',
        'note', 
        "category",
    ]

    def get_success_message(self, cleaned_data):
        """Get message successfuly """
        return self.success_message % dict(name=self.object.name)