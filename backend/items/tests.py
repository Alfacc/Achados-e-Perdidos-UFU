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

    def test_blank_title_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "title": "   "}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("title", res.data)

    def test_invalid_category_has_friendly_message(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "category": 9999}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["category"], ["Selecione uma categoria válida."])

    def test_description_too_long_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "description": "x" * 1001}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("description", res.data)

    def test_client_cannot_forge_status_or_owner(self):
        other = User.objects.create_user("bia@ufu.br", "SenhaForte#2026", name="Bia")
        self.client.force_authenticate(self.user)
        res = self.client.post(
            "/api/items/", {**self.data, "status": "RESOLVED", "owner": other.id}, format="json"
        )
        self.assertEqual(res.status_code, 201)
        item = Item.objects.get()
        self.assertEqual(item.status, "OPEN")
        self.assertEqual(item.owner, self.user)

    def test_non_image_photo_rejected(self):
        self.client.force_authenticate(self.user)
        txt = SimpleUploadedFile("nota.txt", b"nao sou imagem", content_type="text/plain")
        res = self.client.post("/api/items/", {**self.data, "photo": txt}, format="multipart")
        self.assertEqual(res.status_code, 400)
        self.assertIn("photo", res.data)

    @override_settings(MAX_PHOTO_MB=0)
    def test_photo_over_size_limit_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "photo": self._gif()}, format="multipart")
        self.assertEqual(res.status_code, 400)
        self.assertIn("photo", res.data)

    def _gif(self):
        gif = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
               b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
        return SimpleUploadedFile("foto.gif", gif, content_type="image/gif")

    def test_create_with_photo_multipart(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/items/", {**self.data, "photo": self._gif()}, format="multipart")
        self.assertEqual(res.status_code, 201, res.data)
        self.assertTrue(res.data["photo"])
