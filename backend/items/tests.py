import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import Category, Item

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ItemCreateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ana@ufu.br", "SenhaForte#2026", name="Ana")
        self.category = Category.objects.first()
        self.data = {
            "type": "LOST",
            "title": "Garrafa azul",
            "description": "Garrafa térmica azul com adesivos.",
            "category": self.category.id,
            "location": "Bloco 1B, sala 101",
            "date_occurred": "2026-11-03",
        }

    def test_seed_categories_exist(self):
        self.assertGreaterEqual(Category.objects.count(), 5)

    def test_create_requires_login(self):
        res = self.client.post("/api/items/", self.data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_create_lost_item_sets_owner_and_status(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", self.data, format="json")
        self.assertEqual(res.status_code, 201)
        item = Item.objects.get()
        self.assertEqual(item.owner, self.user)
        self.assertEqual(item.status, "OPEN")

    def test_future_date_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "date_occurred": "2999-01-01"}, format="json")
        self.assertEqual(res.status_code, 400)

    def test_create_with_photo_multipart(self):
        self.client.force_authenticate(self.user)
        gif = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
               b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
        photo = SimpleUploadedFile("foto.gif", gif, content_type="image/gif")
        res = self.client.post("/api/items/", {**self.data, "photo": photo}, format="multipart")
        self.assertEqual(res.status_code, 201, res.data)
        self.assertTrue(res.data["photo"])
