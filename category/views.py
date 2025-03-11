from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CategoryForm


@user_passes_test(lambda u: u.is_superuser)  # Ограничиваем доступ только для суперпользователей
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('add-category')  # Переназначаем на ту же страницу
        else:
            messages.error(request, 'Произошла ошибка при добавлении категории.')
    else:
        form = CategoryForm()

    return render(request, 'profile/category_creation.html', {'form': form})