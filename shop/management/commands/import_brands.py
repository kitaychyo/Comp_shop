from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from shop.models import Brand


class Command(BaseCommand):
    help = "Import Brand records from images found in MEDIA_ROOT/brands/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace image path for existing brands with the same title.",
        )

    def handle(self, *args, **options):
        media_brands_dir = Path(settings.MEDIA_ROOT) / "brands"
        if not media_brands_dir.exists():
            self.stderr.write(self.style.ERROR(f"Directory not found: {media_brands_dir}"))
            return

        created, updated, skipped = 0, 0, 0
        for file_path in sorted(media_brands_dir.iterdir()):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}:
                continue

            # Title from filename (without extension), normalize a bit
            raw = file_path.stem
            title = raw.replace("_", " ").replace("-", " ").strip().title()

            image_relative = f"brands/{file_path.name}"

            brand, exists = Brand.objects.get_or_create(
                title=title,
                defaults={
                    "image": image_relative,
                    "description": "",
                },
            )
            if exists:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {title} -> {image_relative}"))
            else:
                if options["replace"]:
                    # Only update image if different
                    if brand.image.name != image_relative:
                        brand.image.name = image_relative
                        brand.save(update_fields=["image"])
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
