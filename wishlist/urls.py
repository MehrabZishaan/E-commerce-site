from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist, name='wishlist'),  # Display the user's wishlist
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add a product to the wishlist
    path('remove_from_wishlist/<int:product_id>/', views.remove_wishlist_item, name='remove_wishlist_item'),  # Remove a product from the wishlist
]
