from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from account.models import Account, Type
from account.mixin import AccountMixinView
# Create your views here.


class AccountListView(ListView):
    """Get All Accounts"""

    paginate_by: int = 5
    model: Account = Account
    template_name: str = "account.html"
    fields: list = [
        "id", 
        "fullname", 
        'phone', 
        'address', 
        "note", 
        'type'
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # filter by fullname 
        queryset = queryset.filter(fullname__contains=self.request.GET.get("search", ''))

       
        if self.request.GET.get("type"):
            # filter by type account 
            queryset = queryset.filter(type__name__contains=self.request.GET.get("type", ''))
        
        return queryset

    def get_context_data(self, **kwargs: dict):

        # limit page 
        self.paginate_by = self.request.GET.get("per_page", self.paginate_by)

        context = super().get_context_data(**kwargs)
        context['fields'] = self.fields # set field names 
        context['per_page'] = self.paginate_by # set per_page 
        context['types'] = Type.objects.all() # get all categories

        return context
    
class AccountCreateView(AccountMixinView, CreateView) :
    """Create new Account"""

    success_message = "Account %(fullname)s was created successfully"

    def form_valid(self, form):
        
        # set current user 
        form.instance.user = self.request.user
        return super().form_valid(form)

    

class AccountUpdateView(AccountMixinView, UpdateView):
    """update Account by id"""

    success_message = "Account %(fullname)s was updated successfully"


class AccountDeleteView(AccountMixinView, DeleteView):
    """Delete Account by id"""

    success_message = "Account %(fullname)s was deleted successfully"
