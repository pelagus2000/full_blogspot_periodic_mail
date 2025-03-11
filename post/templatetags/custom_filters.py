from django import template
import re

register = template.Library()


CURRENCIES_SYMBOLS = {
   'rub': '₽',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'

@register.filter(name='censor')
def censor(value):
    bad_words = ['редиска']
    for word in bad_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub(
            word[0] + '*' * (len(word) - 1),
            value
        )
    return value