from django import forms
from django.core.exceptions import ValidationError
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

