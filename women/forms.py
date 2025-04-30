from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm
from django.forms import Textarea
from .models import Contact

#  обьявляем класс формы описывающую формы добавления в статьи: сlass AddPostForm(forms.Form)
# эта форма не связанна с моделями поэтому потом была заменена на связанную с моделями
# (но она также добавляет в базу данных посты)
# class AddPostForm(forms.ModelForm) # ниже атрибуты класса(поля) названия те же что и в классе #Uroki
#     title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))  # в техлитературе по ссылке есть описание всех полей
#     # widget=forms.TextInput(attrs={'class': 'form-input'}- виджет для присвоения класса #офрмления поля
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows': 10}), #label="Контекст")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True) # #позволяет пользователю отмечать опубликовано или нет
#     cat = forms.ModelChoiceField(queryset=Categor.objects.all(), label="Категории", #empty_label="Категория не выбрана")  # выбор категории
#     # c выпадающего списка

# class AddPostForm(forms.Form)- былсоздан просто для наглядности и по сути
# копировал  class Uroki(models.Model) -такие же поля и др. и не был связан с
# базой данных напрямую если он с ней взаимодействует поэтому для взаимодействия с базой данных #этот класс
# унаследуем от другого класса - class AddPostForm2(forms.ModelForm) см.внизу:

# безверхних пояснений в чистом  виде:


#  Для придания лучшего вида стандартной форме регистрации
#  (класс UserCreationForm) создадим свой класс формы регистрации:

class RegisterUserForm(forms.ModelForm): 
    # дублируем элементы словаря(формы) так как ниже они не срабаьывают
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()  # get_user_model()-функция джанго возвращающая текущую модель
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        label = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
class LoginUserForm(forms.Form): # свой класс авторизации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


#class ContactForm(forms.Form): # на этот класс обратной саязи ссылаемся в views.py
    #name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})) 
    #email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    #message = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'placeholder': #'Сообщение', 'cols': 40, 'rows': 12})) 
    #captcha = CaptchaField()


class ContactForm(forms.ModelForm):

    class Meta:
        # Определяем модель, на основе которой создаем форму
        model = Contact
        # Поля, которые будем использовать для заполнения
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'message': Textarea(
                attrs={
                    'placeholder': 'Напишите тут ваше сообщение'
                }
            )
        }
    def __init__(self, *args, **kwargs): # добавил 4.01.2025 ничего не поменялось

        """

        Обновление стилей формы

        """

        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})



class AddPostForm(forms.ModelForm):
# форма связанная с моделями - наследуется от  класса-ModelForm(когда нужно связать с моделью)
    def __init__(self, *arqs, **kwards): # конструктор который вызывает конструктор
    #базового класса-ModelForm:
        super().__init__(*arqs, **kwards)  # для поля cat меняем свойство empty_label
        self.fields['cat'].empty_label = "Категория не выбрана" # теперь вместо черточек будет

    class Meta: # вложенный класс
        model = Uroki # атрибут model связывает эту форму с моделью Uroki(с ее полями)
        #  fields = '__all__'  # атрибут fields указывает какие поля нужно
        # заполнить  ' __all__- означает все поля кроме тех которые заполняются автоматически но
        # обычно нужно указывать поля и мы указываем все поля кроме фото
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = { # виджет- словарь для каких полей какие применяются стили  
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        # URL в форме можно любой слаг на латине
    def clean_title(self):  # создаем свой пользовательский валидатор, который срабатывает после
# стандартной валидации... обязательно clean с нижним подчеркиванием затем имя поля для которого
# делается валидация. Валидатор(метод) должен сгенирировать исключение ValidationError
        title = self.cleaned_data['title'] # проверяем конкретно название заголовков
        if len(title) > 200: # проверяется
            raise ValidationError("Длина строки превышает 200 символов")

        return title # иначе возвращается заголовок