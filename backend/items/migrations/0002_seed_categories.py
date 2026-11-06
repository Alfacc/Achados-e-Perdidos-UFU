from django.db import migrations

CATEGORIES = [
    "Documentos",
    "Eletrônicos",
    "Chaves",
    "Roupas e acessórios",
    "Material de estudo",
    "Garrafas e utensílios",
    "Outros",
]


def seed(apps, schema_editor):
    Category = apps.get_model("items", "Category")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)


def unseed(apps, schema_editor):
    Category = apps.get_model("items", "Category")
    Category.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):
    dependencies = [("items", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
