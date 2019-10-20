from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from basket.models import Basket
from product.models import Product


class BaseTestCase(TestCase):

  fixtures = ['products.json']

  def setUp(self):
    self.basket = Basket.objects.create()


class TestBasketCreateView(TestCase):

  def test_post(self):
    response = self.client.post(reverse('basket:create'))
    json = response.json()
    self.assertEqual(json['basket_id'], 1)


class TestDetailView(BaseTestCase):

  def test_total_price_empty(self):
    response = self.client.get(reverse('basket:get', kwargs={'pk': 1}))
    json = response.json()
    self.assertEqual(json['total_price'], '0.00')

  def test_total_price_1_product(self):
    self.basket.add_item(
      Product.objects.get(pk=1)
    )
    response = self.client.get(reverse('basket:get', kwargs={'pk': 1}))
    json = response.json()
    self.assertEqual(json['total_price'], '1.99')

  def test_total_price_multiple_products(self):
    p1 = Product.objects.get(pk=1)
    p2 = Product.objects.get(pk=2)
    p3 = Product.objects.get(pk=3)
    self.basket.add_item(p1, 2)
    self.basket.add_item(p2, 3)
    self.basket.add_item(p3, 4)

    expected_price = p1.price * 2 + p2.price * 3 + p3.price * 4

    response = self.client.get(reverse('basket:get', kwargs={'pk': 1}))
    json = response.json()
    self.assertEqual(json['total_price'], str(expected_price))


class TestBasketAddItemView(BaseTestCase):

  @mock.patch.object(Basket, 'add_item')
  def test_form_valid(self, add_item_patch):

    response = self.client.post(reverse('basket:add-item', kwargs={'pk': 1}), {
      'product': 1,
      'quantity': 2,
    })

    add_item_patch.assert_called_once_with(
      Product.objects.get(pk=1),
      2
    )

  def test_form_invalid(self):

    response = self.client.post(reverse('basket:add-item', kwargs={'pk': 1}), {
        'quantity': 2,
    })

    self.assertEqual(response.status_code, 400)


class TestBasketRemoveItemView(BaseTestCase):

  @mock.patch.object(Basket, 'remove_item')
  def test_form_valid(self, remove_item_patch):

    response = self.client.post(reverse('basket:remove-item', kwargs={'pk': 1}), {
        'product': 1,
        'quantity': 2,
    })

    remove_item_patch.assert_called_once_with(
        Product.objects.get(pk=1),
        2
    )

  def test_form_invalid(self):

    response = self.client.post(reverse('basket:remove-item', kwargs={'pk': 1}), {
        'quantity': 2,
    })

    self.assertEqual(response.status_code, 400)


class TestBasketEmptyItemView(BaseTestCase):

  @mock.patch.object(Basket, 'empty')
  def test_form_valid(self, empty_patch):

    response = self.client.post(reverse('basket:empty', kwargs={'pk': 1}), {
        'product': 1,
        'quantity': 2,
    })

    empty_patch.assert_called_once_with()
