from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . forms import LoginUserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from . forms import *
from . models import *  # импортируем все  из файла models.py
# Create your views here.
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . forms import RegisterUserForm
from . forms import LoginUserForm
from django.urls import reverse

# Create your views here.


menu = [{'title': "О сайте", 'url_name': 'about'}, # убрали в 17 уроке
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'}
]

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST) # заполненная форма
        if form.is_valid(): # проверка корректности заполнения формы
            cd = form.cleaned_data # если она корректная то вызывается функция authenticate()
            user = authenticate(request, username=cd['username'], password=cd['password']) 
            # которая проверяет на соотвествие введенных данных
            # с данными в базе если ок проверяется активен ли пользователь(не забанен и т.д)
             # if user and user.is_active если активен-существует
            if user and user.is_active: 
                login(request, user)  # то функция login позволяет войти в систему перенаправляя
                return HttpResponseRedirect(reverse('home'))   # на домашнюю страницу, джанго
                  # через сессии запоминает авторизацию и в следующий раз не надо вводить данные
    
    else: 
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form':form, 'menu': menu}) 


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save() # заносим в базу
            return render(request, 'users/register_done.html', {'menu': menu})
    else:
        form = RegisterUserForm() # возвращаем пустую форму
    return render(request, 'users/register.html', {'form':form, 'menu': menu})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login')) # в пакете конфигурации web/urls
     # дополнительно проптсали пространство имен namespace поэтому не смотря на то что у нас два
     # маршрута по login они не пересекаются и мы можем различать их, users берется с 
     # пространства имен а login как маршрут с приложения women
     # маршруты с приложения users идут с приставкой users



