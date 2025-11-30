from django.shortcuts import render
from insydent.models import Product, Category

# Create your views here.

def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'catalog.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

