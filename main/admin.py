from django.contrib import admin
from .models import Category, MovieDetails, Review

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    """
    category model to the administratio site
    """

    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


class MovieDetailsAdmin(admin.ModelAdmin):
    """
    Movie Review
    """
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(MovieDetails, MovieDetailsAdmin)
admin.site.register(Review)
