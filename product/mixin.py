from product.models import Product
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class ProductMixinView(SuccessMessageMixin):

    # model base-view 
    model: Product = Product

    # successfuly redirect  
    success_url = reverse_lazy("product")

    # message for success 
    success_message = "Product %(name)s was successfully"

    # template form 
    template_name: str = "forms/porduct_form.html"

    # form fields 
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