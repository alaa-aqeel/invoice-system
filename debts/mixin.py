from debts.models import Debt
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class DebtsMixinView(SuccessMessageMixin):

    model: Debt = Debt
    success_url = reverse_lazy("debts")
    success_message = "Debt %(id)s was successfully"
    template_name: str = "forms/debts_form.html"
    fields: list = [
        "account", 
        'price', 
        "note",
    ]

    def get_success_message(self, clean_data):
        """Get message successfuly """
        print(clean_data)
        return self.success_message % dict(id=self.object.id)