from django.contrib import admin
from .models import Category
from modeltranslation.admin import TranslationAdmin

class CategoryAdmin(TranslationAdmin):
    model = Category

admin.site.register(Category, CategoryAdmin)

# Register your models here.
