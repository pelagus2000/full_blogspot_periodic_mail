from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author_name']  # Единственное поле, которое пользователь может изменить
        widgets = {
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Введите псевдоним автора',
                'class': 'form-control',
            }),
        }