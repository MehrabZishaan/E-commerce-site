from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all()
    if not products:
        message = "No products are available at the moment."
        return render(request, 'index.html', {'message': message})
    
    return render(request, 'index.html', {'products': products})