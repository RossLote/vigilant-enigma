from django import forms

from product.models import Product

from .models import Basket


class BasketUpdateForm(forms.Form):
  product = forms.ModelChoiceField(queryset=Product.objects.all())
  quantity = forms.IntegerField(min_value=0, required=False)
