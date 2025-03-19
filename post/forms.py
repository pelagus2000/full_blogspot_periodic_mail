from django import forms
from django.core.exceptions import ValidationError
from .models import Posts
from django.forms.widgets import CheckboxSelectMultiple
from category.models import Category
from django.utils.translation import gettext as _  # импортируем функцию для перевода

class NewsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'body', 'categories']
        widgets = {
            'categories': CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        if body is not None and len(body) < 10:
            raise ValidationError({
                "body": "Описание не может быть менее 20 символов."
            })

        name = cleaned_data.get("name")
        if name == body:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'body', 'categories']
        widgets = {
            'categories': CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        if body is not None and len(body) < 10:
            raise ValidationError({
                "body": "Описание не может быть менее 20 символов."
            })

        name = cleaned_data.get("name")
        if name == body:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }