from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Category, Product


def checkout_page(request, pk):
    category_list = Category.objects.all()
    user = request.user
    item_to_checkout = Product.objects.get(id=pk)
    context = {
        'Item': item_to_checkout,
        'categories': category_list,
        'user': user
    }
    return render(request, 'checkout.html', context)


def home_page(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all().order_by('-date_created')
    sample_products = product_list[:3]
    context = {
        'products': product_list,
        'categories': category_list,
        'sample_products': sample_products
    }
    return render(request, 'home.html', context)


def save_order(request):
    pass
