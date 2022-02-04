from account.models import Account
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class AccountMixinView(SuccessMessageMixin):

    # model base-view 
    model: Account = Account

    # successfuly redirect  
    success_url = reverse_lazy("account")

    # message for success 
    success_message = "Product %(fullname)s was successfully"

    # template form 
    template_name: str = "forms/account_form.html"

    # form fields 
    fields: list = [
        "fullname", 
        'phone', 
        'address', 
        "note", 
        'type'
    ]

    def get_success_message(self, cleaned_data):
        """Get message successfuly """
        
        return self.success_message % dict(fullname=self.object.fullname)