from django.core.management.base import BaseCommand
from shop.models import Category

MAPPING = {
    "Phone": "Смартфоны",
    "Notebook": "Ноутбуки",
    "Headphones": "Наушники",
    "Console": "Игровые приставки",
}

class Command(BaseCommand):
    help = "Localize Category.title to Russian using predefined mapping"

    def handle(self, *args, **options):
        updated = 0
        for en, ru in MAPPING.items():
            try:
                cat = Category.objects.get(title=en)
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Skip: '{en}' not found"))
                continue
            cat.title = ru
            cat.save(update_fields=["title"])
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"Updated: {en} -> {ru}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Updated: {updated}"))
