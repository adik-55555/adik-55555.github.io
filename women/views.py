from django.views.generic import CreateView
from django.forms import ModelForm
from django.forms import Textarea
from .models import Contact
from django.urls import reverse_lazy
from .forms import ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from . forms import * 
from django import forms
from . models import *  # импортируем все  из файла models.py
# Create your views here.
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . forms import RegisterUserForm
from . forms import LoginUserForm
from . forms import ContactForm
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail

#menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"] # переменную menu добавляем в #словарь в функцию index
menu = [{'title': "О сайте", 'url_name': 'about'}, # убрали в 17 уроке
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
       # {'title': "Войти", 'url_name': 'login'}
]

@cache_page(60 * 2) # декоратор для кеширования главной страницы на 2 мин

def index(request): # функцию представления связываем с url адресом в пакете конфигурации(файл 
# web/urls.py)
    #return HttpResponse("Страница приложения women")
    #return render(request, 'women/index.html' ) # заменили  HttpResponse на render далее #добавили переменную ввиде словаря 'title':'Главная страница'
    #posts = Uroki.objects.all() # пееменная-ссылка на все записи в таблице women которую
    #также добавили в словарь для включения в шаблон
    #cats = Categor.objects.all() # выбираем все записи с таблицы сategory
    posts = Uroki.objects.all()   
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    #context = {
        #'posts': posts,
        #'cats' : cats,
        #'menu': menu,
        #'title': 'Главная страница',
        #'cat_selected': 0, # 0 для того чтоб на главной странице отображались все записи
    
     #}
    
    return render(request, 'women/index.html', {'menu': menu, 'posts': posts, 'title':'Главная страница',} ) 
    #return render(request, 'women/index.html', context=context)
    
    # каталог с шаблонами templates джанго найдет сам согласно настроек а путь к данному шаблону
    # women/index.html мы прописываем сами в этом файле

def about(request): # аналогично для шаблона about -этот шаблон делаем на подобе index.html для
    posts = Uroki.objects.all()   
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    #context = {
        #'posts': posts,
        ##'cats' : cats,
        #'menu': menu,
        #'title': 'Главная страница',
        #'cat_selected': 0, # 0 для того чтоб на главной странице отображались все записи
    
     #}
                       
    #return render(request, 'women/about.html', {'page_obj': page_obj, 'posts':posts,
    #'menu':menu})

    return render(request, 'women/about.html', {'posts':posts, 'menu':menu, 'title': 'О сайте'})




def login(request): 
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password']) 
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))    
    
    else: 
        form = LoginUserForm()
    return render(request, 'women/login.html', {'form':form, 'menu': menu})

def register(request):    
    form = RegisterUserForm()
    return render(request, 'women/register.html', {'form':form, 'menu': menu})    

def logout(request):
    #logout(request)
    return HttpResponse("logout")
    
    




def pageNotFound(request, exception):  # пример обработки исключения-отсутствия страницы
    # при переключение в файле настроек на DEBUG = False - в режиме делового применения
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')  # Выведет строку-Страница не #найдена
#def show_post(request, post_id): эту функцию -заглушку заменили в 12 уроке на нижнее
    #return HttpResponse(f"Отображение статьи с id = {post_id}")

def show_post(request, post_id):  #  def show_post(request, post_id):  #поменяли в 12 уроке
    post = get_object_or_404(Uroki, pk=post_id)  # pk=post_id поменяли на slug=... но не получилось
    # post-ссылка на класс Uroki
    context = { # формируем словарь из параметров для передачи в шаблон women/post.html
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)    

   


def show_category(request, cat_id):
    posts = Uroki.objects.filter(cat_id=cat_id)
    #cats = Category.objects.all()
    
    if len(posts) == 0: # если нет поста то выдаст ошибку
        raise Http404()

    paginator = Paginator(posts, 2) # пагинация

    page = request.GET.get('page')
    posts = paginator.get_page(page)    
        
    context = {
        'posts': posts,
        ##'cats' : cats,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        #'cat_selected': cat_id, # если не закомментировать по будут все рубрики а не по 2
    
     }     

    return render(request, 'women/index.html', context=context)
    

def addpage(request): #в 13 уроке сделано через функцию но в 15 уроке тоже поменяли на класс #представления(CreateView)
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES) # request.FILES-для выборки файлов #которые были переданы на сервер из формы (нужно для загрузки фото и др.)
        if form.is_valid():  # проверка корректности заполнения формы
            # print(form.cleaned_data) запись в консоли осостоянии валидации
            #try: убрали с except и добавили form.save()
               #Uroki.objects.create(**form.cleaned_data) # добавляем новую запись в базу данных #при форме не связанной напрямую с базой данных, при связанной на прямую можно #записать это:
               form.save()
               return redirect('home')  # если все прошло успешно делаем редирек на главную #страницу
            #except:  #  в случае ошибки добавляем в отражении общей ошибки на странице
                #form.add_error(None, 'Ошибка добавления поста') #убрали вместе с try
    else:
        form = AddPostForm() # пустая форма
#     #  return HttpResponse("Добавление статьи"м экземпляр класса формы(ссылку form на него) и #импортируем
    return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        if form.is_valid():
            form.save() # при успешной валидации сохраняем в базе данных 
            return redirect('home') # при успешной валидации переходим на главную страницу
    
    else:
        form = ContactForm()        
    
    
    return render(request, 'women/contact.html', {'form': form, 'menu': menu})


