from django import forms
from .models import Comment  # Заменить модель на строчную интерпретацию


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Здесь модель остается неизменной
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
