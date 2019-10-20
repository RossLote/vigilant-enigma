from django.http import JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.views.generic.edit import BaseFormView

from . import forms, models


class BasketView(SingleObjectMixin, View):
  model = models.Basket
  action_name = None

  def dispatch(self, request, *args, **kwargs):

    action = getattr(self, self.action_name)
    if self.action_name != 'create':
      self.basket = self.get_object()
    return action(request)

  def get(self, request):
    return JsonResponse({
      "total_price": self.basket.total_price
    })

  def create(self, request):
    basket = models.Basket.objects.create()
    return JsonResponse({
        "basket_id": basket.pk,
    }, status=201)
    
  def add_item(self, request):
    form = forms.BasketUpdateForm(request.POST)

    if form.is_valid():
      self.basket.add_item(
          form.cleaned_data['product'],
          form.cleaned_data.get('quantity') or 1,
      )

      return JsonResponse({
        "message": "Items added to basket",
        "total_price": self.basket.total_price
      })
    else:
      return JsonResponse({
        "errors": form.errors,
      }, status=400)

  def remove_item(self, request):
    form = forms.BasketUpdateForm(request.POST)

    if form.is_valid():
      self.basket.remove_item(
          form.cleaned_data['product'],
          form.cleaned_data.get('quantity') or 1,
      )

      return JsonResponse({
          "message": "Items removed from basket",
          "total_price": self.basket.total_price
      })
    else:
      return JsonResponse({
          "errors": form.errors,
      }, status=400)

  def empty(self, request):
    self.basket.empty()
    return JsonResponse({
        "message": "Basket emptied",
        "total_price": self.basket.total_price
    })
