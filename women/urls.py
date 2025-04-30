from django.urls import path, re_path
from django.views.decorators.cache import cache_page # для кеширования классов представления
from  .views import  *


urlpatterns = [
      path('', cache_page(60 * 2)(index), name='home'), # http://cx69878-django-q1kyl.tw1.ru/women/ #(/women- была #так так как это
      # предусмотрено было в начале в файле web/urls потом поменяли на пустую строку в web/urls
      # и стало http://cx69878-django-q1kyl.tw1.ru/    без women/
      # name='home'- наименование маршрута при редиректах чтоб исключить явное обозначение
      # (60 * 2) кеширование на 2 минуты(60 сек * 2)
      path('about/', about, name='about'),
      path('addpage/', addpage, name='add_page'),
      path('contact/', contact, name='contact'),
      path('login/', login, name='login'),
      path('logout/', logout, name='logout'),
      path('register/', register, name='register'),
      path('post/<int:post_id>/', show_post, name='post'), # путь к иконке читать пост в 12
      # уроке переделали поиск по слагу
      #path('post/<slug:post_slug>/', show_post, name='post'),
      #path('cats/<int:catid>/', categories), # <int:catid>- разделение категорий по числам  
      # одновременно вносим изменения в views.py в функцию categories
      #path('cats/<slug:cat>/', categories), # меняем цифры на слаги... cat -произвольно зовем
      path('category/<int:cat_id>/', cache_page(60 * 2)(show_category), name='category'),
]