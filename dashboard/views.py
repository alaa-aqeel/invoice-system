from django.shortcuts import render

# Create your views here.

def not_found_page(request, exception):

    return render(request, "errors/404.html", status=404)

def index(request):

    return render(request, "index.html")