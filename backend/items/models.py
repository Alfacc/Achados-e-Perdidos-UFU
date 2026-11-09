from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField("nome", max_length=60, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class Item(models.Model):
    """Objeto perdido (LOST) ou encontrado (FOUND). Mesmo modelo para as duas histórias."""

    class Type(models.TextChoices):
        LOST = "LOST", "Perdido"
        FOUND = "FOUND", "Encontrado"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Em aberto"
        RESOLVED = "RESOLVED", "Resolvido"

    type = models.CharField(max_length=5, choices=Type.choices)
    title = models.CharField("título", max_length=120)
    description = models.TextField("descrição", max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    location = models.CharField("local", max_length=150)
    date_occurred = models.DateField("data em que perdeu/encontrou")
    photo = models.ImageField(upload_to="items/%Y/%m/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"
