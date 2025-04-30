from django.contrib import admin
from .models import Contact

# Register your models here.
from .models import *


class UrokiAdmin(admin.ModelAdmin): # вспомогательный класс-дооформления админпанели
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_liks = ('id', 'title')
    search_fields = ('title', 'content') # запятую не ставим в конце так как болюше одного эл-та
    list_editable = ('is_published',)  # редактируемые колонка (публикации)
    list_filter = ('is_published', 'time_create') # колонка для фильтрации
    prepopulated_fields = {"slug": ("title",)} # url дублируется слагами как и в таблице категорий

class CategorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # запятая обязательна- чтоб был как кортеж а не строка
    prepopulated_fields = {"slug": ("name",)}  # добавлено в 12 уроке для
    # автоматического заполнения поля "slug" при заполнении поля "name"



admin.site.register(Uroki, UrokiAdmin)  # в функции register указываем ту модель которую регистрируем
# для своей админпанели
admin.site.register(Categor, CategorAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass