from decimal import Decimal
from django.db import models

# Create your models here.
class Basket(models.Model):
  user = models.ForeignKey(
    'auth.User',
    on_delete=models.PROTECT,
    null=True, # baskets can belong to anonymous users
  )

  @property
  def total_price(self):
    total_price = self.items.aggregate(
        total_price=models.Sum(
          models.F('quantity') * models.F('product__price'),
          output_field=models.DecimalField(decimal_places=2),
        )
    )['total_price'] or Decimal('0')
    return Decimal(total_price).quantize(Decimal('.01'))

  def add_item(self, product, quantity=1):
    item, created = self.items.get_or_create(product=product, defaults={
      'quantity': quantity,
    })

    if not created:
      item.quantity += quantity
      item.save()

  def remove_item(self, product, quantity=None):
    try:
      item = self.items.get(product=product)
      if quantity is None or quantity == item.quantity:
        item.delete()
      else:
        item.quantity -= quantity
        item.save()
    except BasketItem.DoesNotExist:
      pass

  def empty(self):
    self.items.all().delete()

  

class BasketItem(models.Model):
  basket = models.ForeignKey(Basket, related_name='items', on_delete=models.PROTECT)
  product = models.ForeignKey('product.Product', on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField()

  class Meta:
    unique_together = ('basket', 'product')
