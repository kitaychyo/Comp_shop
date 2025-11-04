from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from shop.models import Category


class Command(BaseCommand):
    help = "Import Category records from images found in MEDIA_ROOT/categories/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace image path for existing categories with the same title.",
        )

    def handle(self, *args, **options):
        media_categories_dir = Path(settings.MEDIA_ROOT) / "categories"
        if not media_categories_dir.exists():
            self.stderr.write(self.style.ERROR(f"Directory not found: {media_categories_dir}"))
            return

        created, updated, skipped = 0, 0, 0
        for file_path in sorted(media_categories_dir.iterdir()):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}:
                continue

            raw = file_path.stem
            title = raw.replace("_", " ").replace("-", " ").strip().title()

            image_relative = f"categories/{file_path.name}"

            cat, exists = Category.objects.get_or_create(
                title=title,
                defaults={
                    "image": image_relative,
                },
            )
            if exists:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {title} -> {image_relative}"))
            else:
                if options["replace"]:
                    if cat.image.name != image_relative:
                        cat.image.name = image_relative
                        cat.save(update_fields=["image"])
                        updated += 1
                        self.stdout.write(self.style.WARNING(f"Updated: {title} -> {image_relative}"))
                    else:
                        skipped += 1
                else:
                    skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created}, Updated: {updated}, Skipped: {skipped}"
            )
        )
