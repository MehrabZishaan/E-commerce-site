from django.db import models
from store.models import Product
from django.contrib.auth.models import User
from django.conf import settings

from accounts.models import Account  # Import the Account model from the accounts app

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Wishlist for {self.user.username}'

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.product_name} in {self.wishlist.user.username}\'s wishlist'

# class Wishlist(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Wishlist for {self.user.username}'