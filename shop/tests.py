from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from shop.models import Goods
from taggit.models import Tag


class GoodsListViewAPITest(APITestCase):
    url_name = reverse('list-goods')

    def setUp(self):
        """Создает товары и тэги перед каждым тестом"""
        tag1 = Tag.objects.create(name='electronics')
        tag2 = Tag.objects.create(name='clothing')
        tag3 = Tag.objects.create(name='home_appliances')
        tag4 = Tag.objects.create(name='cars')
        tag5 = Tag.objects.create(name='shrek')

        self.goods1 = Goods.objects.create(name='Product1', description='Description of product 1')
        self.goods2 = Goods.objects.create(name='Product2', description='Description of product 2')
        self.goods3 = Goods.objects.create(name='Product3 special', description='Description of product 3 special')
        self.goods4 = Goods.objects.create(name='Product4')
        self.goods5 = Goods.objects.create(name='Another1')
        self.goods6 = Goods.objects.create(name='Another2')

        self.goods1.tags.add(tag1, tag2)
        self.goods2.tags.add(tag3)
        self.goods3.tags.add(tag1)
        self.goods4.tags.add(tag2)
        self.goods5.tags.add(tag4)
        self.goods6.tags.add(tag5)

    def test_filter_by_name(self):
        """Тестирование фильтрации по имени товара"""
        response = self.client.get(self.url_name, {'name': 'Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Название 'Product' содержат 4 товара
        response2 = self.client.get(self.url_name, {'name': 'another'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 2)  # Название 'Another' содержат 2 товара


    def test_filter_by_description(self):
        """Тестирование фильтрации по описанию товара"""
        response = self.client.get(self.url_name, {'description': 'special'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем лишь один товар с 'особенным' описанием
        self.assertEqual(response.data[0]['name'], 'Product3 special')
        response2 = self.client.get(self.url_name, {'description': 'description'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 3)  # Только три товара содержат описание


    def test_filter_by_tag(self):
        """Тестирование фильтрации по тегу товара"""
        response = self.client.get(self.url_name, {'tag': 'electronics'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ожидаем 2 товара с тегом 'electronics'
        response2 = self.client.get(self.url_name, {'tag': 'cloth'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 2)  # Ожидаем 2 товара содержащих тэг 'cloth'


    def test_multiple_filters(self):
        """Тестирование фильтрации по нескольким параметрам"""
        response = self.client.get(self.url_name, {'name': 'Product', 'tag': 'shrek'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)  # Название 'Product' или тэг 'shre' содержат пять товаров
        response2 = self.client.get(self.url_name, {'name': 'Anoth', 'tag': 'electron'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 4)  # Название 'Anoth' или тэг 'electron' содержат четыре товара

    def test_without_filters(self):
        """Query параметры не передаются"""
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6) # Вернутся все 6 товаров
