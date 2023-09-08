from .models import WishlistItem
from .views import _wishlist_id

def wishlist_counter(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return {}
    else:
        wishlist_id = request.session.get('wishlist_id')
        if isinstance(wishlist_id, int):  # Check if wishlist_id is an integer
            try:
                wishlist_items = WishlistItem.objects.filter(wishlist_id=wishlist_id)
                for wishlist_item in wishlist_items:
                    wishlist_count += 1
            except WishlistItem.DoesNotExist:
                wishlist_count = 0
        else:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)
