from django.contrib import admin
from .models import Category, Size, Color
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name', 'slug')
    
admin.site.register(Category, CategoryAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Size, SizeAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Color, ColorAdmin)

