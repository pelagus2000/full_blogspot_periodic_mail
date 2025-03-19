from django.contrib import admin
from .models import Posts
from category.models import Category
from django.contrib import messages
from modeltranslation.admin import TranslationAdmin


@admin.action(description="Удалить все новости из указанной категории")
def delete_news_by_category(modeladmin, request, queryset):
    # Проверяем, что была выбрана только одна категория
    if queryset.count() != 1:
        messages.error(request, "Выберите только одну категорию.")
        return

    category = queryset.first()
    posts_to_delete = Posts.objects.filter(categories=category)

    if not posts_to_delete.exists():
        messages.warning(request, f"В категории '{category.name}' нет новостей для удаления.")
        return

    post_titles = [post.title for post in posts_to_delete]
    count, _ = posts_to_delete.delete()
    messages.success(
        request,
        f"Удалено {count} новостей из категории '{category.name}': {', '.join(post_titles)}"
    )

class PostsAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Posts

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = "Категории"

    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'preview', 'author', 'display_categories') # оставляем только имя и цену товара
    list_filter = ('author', 'categories') # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'date') # тут всё очень похоже на фильтры из запросов в базу
    actions = [delete_news_by_category] # добавляем действия в список



admin.site.register(Posts, PostsAdmin)
