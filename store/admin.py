from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category', 'stock', 'created_date', 'modified_date', 'is_available', 'display_sizes', 'display_colors']
    prepopulated_fields = {'slug': ('product_name',)}

    def display_sizes(self, obj):
        return ', '.join([size.name for size in obj.sizes.all()])

    def display_colors(self, obj):
        return ', '.join([color.name for color in obj.colors.all()])

    display_sizes.short_description = 'Sizes'
    display_colors.short_description = 'Colors'

admin.site.register(Product, ProductAdmin)
