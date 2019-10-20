from django.test import Client, TestCase

from basket.models import Basket
from product.models import Product

class BasketModelAddItemTestCase(TestCase):

  fixtures = ['products.json']

  def setUp(self):
    self.basket = Basket.objects.create()

  def test_add_item_with_default_quantity(self):
    product = Product.objects.get(pk=1)

    self.basket.add_item(product)

    items = self.basket.items.all()
    item = items[0]
    
    self.assertEqual(items.count(), 1)
    self.assertEqual(item.product, product)
    self.assertEqual(item.quantity, 1)

  def test_add_item_with_specific_quantity(self):
    product = Product.objects.get(pk=1)

    self.basket.add_item(product, 3)

    items = self.basket.items.all()
    item = items[0]

    self.assertEqual(items.count(), 1)
    self.assertEqual(item.product, product)
    self.assertEqual(item.quantity, 3)

  def test_add_item_using_topup(self):
    product = Product.objects.get(pk=1)

    self.basket.add_item(product, 3)
    items = self.basket.items.all()
    item = items[0]
    self.assertEqual(item.quantity, 3)

    self.basket.add_item(product, 2)
    items = self.basket.items.all()
    item = items[0]
    self.assertEqual(item.quantity, 5)

  def test_add_second_item(self):
    product1 = Product.objects.get(pk=1)
    product2 = Product.objects.get(pk=2)

    self.basket.add_item(product1, 2)
    self.assertEqual(self.basket.items.count(), 1)

    self.basket.add_item(product2, 3)
    self.assertEqual(self.basket.items.count(), 2)


    item1 = self.basket.items.get(product=product1)
    self.assertEqual(item1.product, product1)
    self.assertEqual(item1.quantity, 2)

    item2 = self.basket.items.get(product=product2)
    self.assertEqual(item2.product, product2)
    self.assertEqual(item2.quantity, 3)


class BasketModelRemoveItemTestCase(TestCase):

  fixtures = ['products.json']

  def setUp(self):
    self.product1 = Product.objects.get(pk=1)
    self.product2 = Product.objects.get(pk=2)

    self.basket = Basket.objects.create()
    self.basket.items.create(
      product=self.product1,
      quantity=5,
    )
    self.basket.items.create(
      product=self.product2,
      quantity=3,
    )

  def test_remove_item_with_quantity_less_than_amount_in_basket(self):

    self.basket.remove_item(self.product1, 3)
    items = self.basket.items.all()

    self.assertEqual(items.count(), 2)

    item = self.basket.items.get(product=self.product1)
    self.assertEqual(item.quantity, 2)

  def test_remove_item_with_default_quantity(self):

    self.basket.remove_item(self.product2)
    items = self.basket.items.all()

    self.assertEqual(items.count(), 1)

    item = self.basket.items.get(product=self.product1)
    self.assertEqual(item.quantity, 5)

  def test_remove_item_not_present_in_basket(self):
    product = Product.objects.get(pk=3)
    self.basket.remove_item(product)
    items = self.basket.items.all()

    self.assertEqual(items.count(), 2)


class BasketModelTestCase(TestCase):

  fixtures = ['products.json']

  def setUp(self):
    self.product1 = Product.objects.get(pk=1)
    self.product2 = Product.objects.get(pk=2)

    self.basket = Basket.objects.create()
    self.basket.items.create(
        product=self.product1,
        quantity=5,
    )
    self.basket.items.create(
        product=self.product2,
        quantity=3,
    )

  def test_empty(self):
    items = self.basket.items.all()
    self.assertEqual(items.count(), 2)

    self.basket.empty()

    items = self.basket.items.all()
    self.assertEqual(items.count(), 0)

  def test_total_price(self):
    price1 = self.product1.price * 5
    price2 = self.product2.price * 3

    self.assertEqual(self.basket.total_price, price1+price2)
