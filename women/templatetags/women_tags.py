
from django import template # template-модуль для работы с шаблонами 
from women.models import *  # все модели в приоложении models.py
# для корректности кода нужно исключить повторение строк кода в разных местах и файлах
# для этого создается в
# директории women папка для пользовательских(собственных) тегов в ней создаются  файл __init__(подчеркивающий что это папка пакетная директория и файл women_tags.py

# Создаем экземпляр класса Library() для регистрации всех пользовательских шаблонных тегов:

register = template.Library()  # читается так -в модуле template создаем экземпляр класса
# (объект) Library ну а register-ссылка на него

@register.simple_tag(name='getcats')   # simple_tag()- декоратор из класса Library превращающий
# функцию  get_categories() в пользовательский тег который можно использовать в наших шаблонах
# вставляя в них фрагмент чего то, name='getcats- произвольное имя пользовательского тега
# которое вставляется в шаблон base.html с передачей содержимого ссылке categories

def get_categories(filter=None):  # произвольная функция для возврата всех категорий
    # filter- именованный параметр который добавили чуть позже и присвоили начальное
    # значение None
    if not filter:
        return Categor.objects.all()
    else:
        return Categor.objects.filter(pk=filter)  # обращение к базе данных и выборка всех #записей из
    # таблицы Categor которые будут возвращаться функцией get_categories():

@register.inclusion_tag('women/list_categories.html') # включающий пользовательский тег который в
def show_categories(sort=None, cat_selected=0):  # возвращает готовый фрагмент html (например #список)автоматически в html шаблон 'women/list_categories.html' который как тег вставляется
# в base.html (в нашем случае-show_categories который возвращает список категорий- html,css...)
    if not sort:
        cats = Categor.objects.all()  # эта функция будет читать все записи с таблицы
        # Categor и возвращать словарь с параметром "cats" и соответствующими данными с списка #cats в шаблон 
    else:
        cats = Categor.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}