from django.db import models
#from django.urls import reverse # выдает 500 ошибку при устр-ве ссылки на чтение постов
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.






class Uroki(models.Model): # Uroki- произвольное название класса базы данных и таблицы в ней
    # этот класс мы наследуем от базового класса Model (поле id уже  автоматически прописаноо #согласно этого класса)
    title = models.CharField(max_length=255, verbose_name="Заголовок") # прописываем остальные #поля models- модуль(файл с кодом который
    # можно повторно использовать   CharField- класс по созданию текстового поля)
    # перечень классов и их характеристики в учебнике по djanco в ссылках)
    # verbose_name="Заголовок"- для изменения в админпанеле названия на нужное (было title)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # slug добавили в 12 уроке для того чтоб использовать слаги в строке запроса но не получилось
    # unique=True- означает уникальность поля, db_index=True - поле будет индексировано
    content = models.TextField(blank=True, verbose_name="Текст статьи") # класс по созданию #контекста и т.д соотсетственно ниже
    photo = models.ImageField(upload_to="photos/%Y/$m/%d/", verbose_name="Фото")  # "photos/%Y/#$m/%d/"- путь к каталогу куда будут загружаться фото(
    # каталлоги и подкаталлоги    /%Y/$m/%d/- шаблон сортировки типа год месяц и дата #распределения)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания") # #поле- время создания статьи (создается автоматич)
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")   # поле #-время последнего редактирования статьи(автоматич)
    is_published = models.BooleanField(default=True, verbose_name="Публикация")    # создается #автоматически так как и здесь значение True
    #cat = models.ForeignKey('Categor', on_delete=models.PROTECT, null=True,verbose_name="Категория")    #добавленный ключ cat.id(.#id-добавляется автоматически)
    cat = models.ForeignKey('Categor', on_delete=models.PROTECT, verbose_name="Категории")  # #заменили верхнюю
    # PROTECT - запрещается удалять категории на которые есть ссылки в таблице women (class #Women)
    # null-временно чтоб создать вторую таблицу потом уберем
    # 'Category'-класс(таблица) ввиде строки так как этот класс определен ниже класса Women ( #если разместить выше то
    # можно писать без ковычек(не как строку), без null=True джанго не добавит ключ так как  #таблица Категории пустая -не создана
    def __str__(self): # эта функция появляется в середине
            # 5 видеоурока для получения заголовка в админпанеле записи при использовании ORM в #консоли джанго.
        return self.title
          
    def get_absolute_url(self): # метод для обращения к конкретной записи в базе данных
            # в админпанеле появляется ссылка с надписью "смотреть на сайте"
        return reverse('post', kwargs={'post_id': self.pk})   # id и pk поменяли на slug  в #12 #уроке но выдало ошибку и вернул назад но лучше исользовать 


    class Meta:
        verbose_name = 'html,css и python' # поменяли название в админпанеле
        verbose_name_plural = 'html, css и python' # чтоб убрать автоматическое добавление s(множ.число)
        #ordering = ['-time_create', 'title'] # сортировка -редактирование записей по времени #создания
        ordering = ['id', 'title'] # сортировка по номеру - id






class Categor(models.Model):  # создаем вторую таблицу Category с двумя полями id
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self): # метод для обращения к конкретной записи в базе данных
        return reverse('category', kwargs={'cat_id': self.pk})   # id и pk поменяли на slug  в #12 уроке # то же как верхняя выдает ошибку 500

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)

    def __str__(self):
        # Будет отображаться следующее поле в панели администрирования
        return f'Вам письмо от {self.email}'        





     

