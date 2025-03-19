from .models import Category
from modeltranslation.translator import translator, register, TranslationOptions
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )  # указываем, какие именно поля надо переводить в виде кортежа

# translator.register(Category, CategoryTranslationOptions)
