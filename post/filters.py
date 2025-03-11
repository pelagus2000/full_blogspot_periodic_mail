import django_filters
from django_filters import ModelChoiceFilter, DateFilter
from django.forms.widgets import DateInput
from .models import Posts
from category.models import Category


class PostsFilter(django_filters.FilterSet):
    category_name = ModelChoiceFilter(
        field_name='categories__name',
        queryset=Category.objects.all(),
        label='Search by category',
    )
    date_after = DateFilter(
        field_name='date',
        lookup_expr='gte',  # greater than or equal (позже или в указанную дату)
        label='Published after',
        widget=DateInput(attrs={
            'type': 'date',  # HTML5 элемент даты
            'class': 'form-control',  # Bootstrap класс для стилей (по желанию)
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Удаляем пустые параметры из фильтра
        for field_name in list(self.data.keys()):
            if self.data[field_name] == '':
                self.data = self.data.copy()
                self.data.pop(field_name)

    class Meta:  # Отступ здесь исправлен
        model = Posts
        fields = {
            'title': ['icontains'],
        }
