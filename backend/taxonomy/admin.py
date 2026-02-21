from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "taxonomy_type", "parent", "active", "region_code")
    list_filter = ("taxonomy_type", "active", "region_code")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
