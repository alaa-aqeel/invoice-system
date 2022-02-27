from django.utils import timezone
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from debts.models import Debt
from debts.mixin import DebtsMixinView
# Create your views here.


class DebtsListView(ListView):
    """Get All Accounts"""

    paginate_by: int = 10
    model: Debt = Debt
    template_name: str = "debt.html"
    fields: list = [
        "id", 
        "account", 
        'price', 
        'created_date',
        'updated_date',
        "user",
    ]

    
    def get_queryset(self) :# { 
        search = self.request.GET.get("search", "")
        
        queryset = super().get_queryset().filter(deleted_at=None).order_by('id')
        # filter by account name or user username 
        queryset = queryset.filter(account__fullname__contains=search )

        return queryset
    # }

    def get_context_data(self, **kwargs): #{ 
        # set limit items 
        self.paginate_by = self.request.GET.get("per_page", self.paginate_by)
        context = super().get_context_data(**kwargs)
        context["fields"] = self.fields # set fields for datatable
        context['per_page'] = self.paginate_by # set per_page in response 
        return context
    # }


class DebtsCreateView(DebtsMixinView, CreateView):
    """Create Debt"""

    def form_valid(self, form):# { 
        # set user created by 
        form.instance.user = self.request.user
        return super().form_valid(form)
    # } 


class DebtsUpdateView(DebtsMixinView, UpdateView):
    """update Debts by id"""
    success_message = "Debt %(id)s was updated successfully"


class DebtsDeleteView(DebtsMixinView, DeleteView): 
    """Delete Debts by id"""
    success_message = "Debt %(id)s was deleted successfully"

    def dispatch(self, request, *args, **kwargs):# { 
        current_object = self.get_object()
        current_object.deleted_at = timezone.now()
        current_object.save()
        return HttpResponseRedirect(self.success_url)
    # } 