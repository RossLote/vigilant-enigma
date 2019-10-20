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

# class BaseBasketView(BaseDetailView):
#   model = models.Basket


# class BaseBasketFormFiew(BaseBasketView, BaseFormView):
#   http_method_names = ['post']
#   form_class = forms.BasketUpdateForm

#   def form_invalid(self, form):
#     return JsonResponse({
#         "message": "",
#         "errors": form.errors,
#     }, status=400)


# class BasketCreateView(View):
#   http_method_names = ['post']
  
#   def post(self, request, *args, **kwargs):
#     basket = models.Basket.objects.create()
#     return JsonResponse({
#       "basket_id": basket.pk,
#     }, status=201)


# class BasketView(BaseBasketView):
#   http_method_names = ['get']

#   def get_context_data(self, **kwargs):
#     ctx = super().get_context_data(**kwargs)
#     context = {
#       'total_price': self.object.total_price,
#     }
#     return context

#   def render_to_response(self, context):
#     return JsonResponse(context)


# class BasketAddItemView(BaseBasketFormFiew):

#   def form_valid(self, form):
#     basket = self.get_object()
#     basket.add_item(
#       form.cleaned_data['product'],
#       form.cleaned_data.get('quantity') or 1,
#     )

#     return JsonResponse({"message": "Items added to basket"})


# class BasketRemoveItemView(BaseBasketFormFiew):
#   http_method_names = ['post']

#   def form_valid(self, form):
#     basket = self.get_object()
#     basket.remove_item(
#         form.cleaned_data['product'],
#         form.cleaned_data.get('quantity'),
#     )
#     return JsonResponse({"message": "Items removed to basket"})


# class BasketEmptyView(BaseBasketView):
#   http_method_names = ['post']

#   def post(self, request, pk):
#     basket = self.get_object()
#     basket.empty()

#     return JsonResponse({"message": "Basket emptied"})
