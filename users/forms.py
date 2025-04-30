from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form): # свой класс авторизации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RegisterUserForm(forms.ModelForm): 
    # дублируем элементы словаря(формы) так как ниже они не срабаьывают
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput()) 
    # password2-в базу данных не заноситься а используется для сопоставления

    class Meta:
        model = get_user_model()  # get_user_model()-функция джанго возвращающая текущую модель
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        label = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        } 

    def clean_password2(self): # проверка на соответствие пароля
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password'] 

    def clean_email(self): # проверка на уникальность email
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

