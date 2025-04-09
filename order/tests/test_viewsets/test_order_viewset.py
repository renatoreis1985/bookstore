import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):
    def setUp(self):
        # Criação de usuário e autenticação
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Criação de categoria e produto para o pedido
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )

    def test_order(self):
        # Cria um pedido para o teste de listagem
        self.order = OrderFactory(user=self.user, product=[self.product])

        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        data = json.dumps({
            "products_id": [self.product.id],
            "user": self.user.id
        })

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Recupera o último pedido criado
        created_order = Order.objects.filter(user=self.user).latest("id")
        self.assertEqual(created_order.user, self.user)
        self.assertIn(self.product, created_order.product.all())