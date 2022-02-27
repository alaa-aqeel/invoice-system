from account.models import Account
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class AccountMixinView(SuccessMessageMixin):

    model: Account = Account
    success_url = reverse_lazy("account")
    success_message = "Product %(fullname)s was successfully"
    template_name: str = "forms/account_form.html"
    fields: list = [
        "fullname", 
        'phone', 
        'address', 
        'type',
        "note", 
    ]

    def get_success_message(self, cleaned_data):
        """Get message successfuly """
        return self.success_message % dict(fullname=self.object.fullname)