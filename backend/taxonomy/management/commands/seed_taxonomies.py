import yaml
import os
from django.core.management.base import BaseCommand
from taxonomy.models import Category, TaxonomyType
from django.utils.text import slugify
from django.conf import settings


class Command(BaseCommand):
    help = "Seed taxonomy categories from YAML files"

    def handle(self, *args, **options):
        self.stdout.write("Seeding taxonomies...")

        self.seed_file("materials.yaml", TaxonomyType.MATERIAL)
        self.seed_file("services.yaml", TaxonomyType.SERVICE)
        self.seed_file("projects.yaml", TaxonomyType.PROJECT)
        self.seed_file("property.yaml", TaxonomyType.PROPERTY)
        self.seed_file("finance.yaml", TaxonomyType.FINANCE)

        self.stdout.write(self.style.SUCCESS("Taxonomy seeding complete."))

    def seed_file(self, filename, taxonomy_type):
        path = os.path.join(settings.BASE_DIR, "taxonomy", "seeds", filename)
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"File not found: {path}"))
            return

        with open(path) as f:
            data = yaml.safe_load(f)

        if not data:
            return

        root_key = list(data.keys())[0]
        categories = data[root_key]

        for item in categories:
            for parent_name, children in item.items():
                parent_obj, _ = Category.objects.get_or_create(
                    name=parent_name,
                    taxonomy_type=taxonomy_type,
                    defaults={'slug': slugify(parent_name)}
                )

                if children:
                    for child_name in children:
                        Category.objects.get_or_create(
                            name=child_name,
                            taxonomy_type=taxonomy_type,
                            parent=parent_obj,
                            defaults={'slug': slugify(child_name)}
                        )
        
        self.stdout.write(f"Seed complete for {taxonomy_type}")
