from .models import Posts
from modeltranslation.translator import translator, register, TranslationOptions
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться

@register(Posts)
class PostsTranslationOptions(TranslationOptions):
    fields = ('title', 'body') # указываем, какие именно поля надо переводить в виде кортежа

# translator.register(Posts, PostsTranslationOptions)
