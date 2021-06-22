from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product

class productModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_product = Product.objects.create(
            purchaser = test_user,
            name = 'name of Product',
            description = 'Words about the Product'
        )
        test_product.save()

    def test_Product_content(self):
        product = Product.objects.get(id=1)

        self.assertEqual(str(product.purchaser), 'tester')
        self.assertEqual(product.name, 'name of Product')
        self.assertEqual(product.description, 'Words about the Product')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_product = Product.objects.create(
            purchaser = test_user,
            name = 'name of Product',
            description = 'Words about the Product'
        )
        test_product.save()

        response = self.client.get(reverse('product_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'name': test_product.name,
            'description': test_product.description,
            'purchaser': test_user.id,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('product_list')
        data = {
            "name":"Testing is Fun!!!",
            "description":"when the right tools are available",
            "purchaser":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, data['name'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_product = Product.objects.create(
            purchaser = test_user,
            name = 'name of Product',
            description = 'Words about the Product'
        )

        test_product.save()

        url = reverse('product_detail',args=[test_product.id])
        data = {
            "name":"Testing is Still Fun!!!",
            "purchaser":test_product.purchaser.id,
            "description":test_product.description,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Product.objects.count(), test_product.id)
        self.assertEqual(Product.objects.get().name, data['name'])


    def test_delete(self):
        """Test the api can delete a product."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_product = Product.objects.create(
            purchaser = test_user,
            name = 'name of Product',
            description = 'Words about the Product'
        )

        test_product.save()

        product = Product.objects.get()

        url = reverse('product_detail', kwargs={'pk': product.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)