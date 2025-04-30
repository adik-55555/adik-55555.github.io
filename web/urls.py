"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from women.views import *
from django.conf import settings
from django.conf.urls.static import static
from women.views import ContactForm
# from debug_toolbar.toolbar import debug_toolbar_urls выдает ошибку- toolbar у меня не открылся
  
    
urlpatterns = [
    path('admin/', admin.site.urls),
        #path('women/', index), # http://cx69878-django-q1kyl.tw1.ru/women/
        #path('cats/', categories) # http://cx69878-django-q1kyl.tw1.ru/cats/
        # заменили две верхние записи на нижнюю:
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace="users")),
    #path('', ContactCreate.as_view(), name='contact_page'),
    #path('success/', success, name='success_page')    
    ] 




handler404 = pageNotFound  #  переменной handler404 присваиваем ссылку на обработчик ошибок
# 404  функцию-pageNotFounв которую прописываем и импортируем в файле views.py
#  для  отражению несуществующих страниц. Вообще в файле settings.py DEBUG = True  # в режиме отладки если False то
#  будет в режиме делового применения и тогда подробное описание предусмотренное для наладки ни
#  к чему. можно предусмотреть другое-короткое описание для режима DEBUG = False- страница не
# найдена


