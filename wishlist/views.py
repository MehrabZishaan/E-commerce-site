from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def _wishlist_id(request):
    if request.user.is_authenticated:
        # User is authenticated, create a wishlist for the user
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_id = wishlist.id
    else:
        # User is not authenticated, create a wishlist without associating it with a user
        wishlist, created = Wishlist.objects.get_or_create(user=None)
        wishlist_id = wishlist.id
    
    if 'wishlist_id' not in request.session:
        request.session['wishlist_id'] = wishlist_id
    
    return wishlist_id

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_id = _wishlist_id(request)
    wishlist = Wishlist.objects.get(id=wishlist_id)

    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
        # Item is already in the wishlist, do something (e.g., show a message)
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(product=product, wishlist=wishlist)
    
    return redirect('wishlist')

@login_required(login_url='login')
def remove_wishlist_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_id = _wishlist_id(request)
    wishlist = Wishlist.objects.get(id=wishlist_id)

    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
        wishlist_item.delete()
    except WishlistItem.DoesNotExist:
        # Handle the case where the item was not in the wishlist (e.g., show a message)
        pass
    
    return redirect('wishlist')

@login_required(login_url='login')
def wishlist(request):
    wishlist_id = _wishlist_id(request)
    wishlist = Wishlist.objects.get(id=wishlist_id)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

    context = {
        'wishlist_items': wishlist_items,
    }

    return render(request, 'wishlist/wishlist.html', context)
