from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category, Size, Color
from django.core.paginator import Paginator
from .forms import SortForm, ReviewForm
from django.db.models import Q
from cart.views import _cart_id
from cart.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

def store(request, category_slug=None):
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_category = None
    selected_size = None
    selected_color = None
    selected_sort = request.GET.get('sort_by', 'default')  # Get the selected sorting option, default to 'default'

    # Get selected category
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=selected_category)
    else:
        products = Product.objects.filter(is_available=True)

    # Get selected size
    size_param = request.GET.get('size')
    if size_param:
        # Filter products based on selected_size
        products = products.filter(sizes__name=size_param)

    # Get selected color
    color_param = request.GET.get('color')
    if color_param:
        # Filter products based on selected_color
        products = products.filter(colors__name=color_param)

    # Sort the products based on the selected_sort option
    if selected_sort == 'price_low_high':
        products = products.order_by('price')
    elif selected_sort == 'price_high_low':
        products = products.order_by('-price')
    elif selected_sort == 'name_az':
        products = products.order_by('product_name')
    elif selected_sort == 'name_za':
        products = products.order_by('-product_name')

    product_count = products.count()  # Calculate the product count here.

    # Pagination
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    sort_form = SortForm(initial={'sort_by': selected_sort})

    context = {
        'products': paged_products,
        'categories': categories,
        'selected_category': selected_category,
        'sizes': sizes,
        'selected_size': selected_size,
        'colors': colors,
        'selected_color': selected_color,
        'sort_form': sort_form,
        'p_count': product_count, 
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Filter products based on keyword in description or product name
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    else:
        products = Product.objects.none()  # No keyword provided, return an empty queryset.

    context = {
        'products': products.order_by('-created_date'),  # Order the filtered products.
        'p_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)