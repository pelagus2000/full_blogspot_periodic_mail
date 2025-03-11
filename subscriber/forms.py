
from django import forms
from .models import Subscriber
from category.models import Category


class SubscriberForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Позволяем выбирать категории
        required=True,  # Категории обязательны
        widget=forms.CheckboxSelectMultiple,  # Можно использовать выпадающий список или чекбоксы
        label="Категории",
    )

    class Meta:
        model = Subscriber
        fields = ['email']  # Указываем только поле email

    def save(self, commit=True):
        """
        Переопределяем метод save, чтобы учесть связь через CategoryMail
        """
        instance = super().save(commit=False)  # Сохраняем только подписчика
        if commit:
            instance.save()  # Сохраняем модель
            # Удаляем существующие связи и добавляем новые
            categories = self.cleaned_data['categories']
            from author.models import CategoryMail
            for category in categories:
                CategoryMail.objects.create(subscriber3=instance, category3=category)
        return instance
