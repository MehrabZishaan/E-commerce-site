from django import forms
from .models import ReviewRating

class SortForm(forms.Form):
    SORT_CHOICES = [
        ('default', 'Default'),
        ('price_low_high', 'Price: Low to High'),
        ('price_high_low', 'Price: High to Low'),
        ('name_az', 'Name: A to Z'),
        ('name_za', 'Name: Z to A'),
    ]
    
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']