from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    payload = {"name": "Maria", "email": "maria@ufu.br", "password": "SenhaForte#2026"}

    def test_register_with_ufu_email(self):
        res = self.client.post("/api/auth/register/", self.payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertNotIn("password", res.data)

    def test_register_rejects_other_domains(self):
        res = self.client.post(
            "/api/auth/register/", {**self.payload, "email": "maria@gmail.com"}, format="json"
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.data)

    def test_register_rejects_duplicate_email_any_case(self):
        self.client.post("/api/auth/register/", self.payload, format="json")
        res = self.client.post(
            "/api/auth/register/", {**self.payload, "email": "MARIA@ufu.br"}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    def test_register_rejects_weak_password(self):
        res = self.client.post(
            "/api/auth/register/", {**self.payload, "password": "12345678"}, format="json"
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("password", res.data)

    def test_login_returns_tokens_and_user(self):
        self.client.post("/api/auth/register/", self.payload, format="json")
        res = self.client.post(
            "/api/auth/login/",
            {"email": "Maria@UFU.br", "password": self.payload["password"]},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.data["user"]["email"], "maria@ufu.br")

    def test_login_wrong_password(self):
        self.client.post("/api/auth/register/", self.payload, format="json")
        res = self.client.post(
            "/api/auth/login/", {"email": "maria@ufu.br", "password": "errada"}, format="json"
        )
        self.assertEqual(res.status_code, 401)

    def test_me_requires_authentication(self):
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
