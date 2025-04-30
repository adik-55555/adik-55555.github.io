from django.test import TestCase

# Create your tests here.


<!-- Заменили шаблон base.html в седьмом уроке на готовый
 Для того чтобы небыло повторений кода в шаблоннах создается базовый шаблон 
в дальнейшем создаются дочерние шаблоны при необходимости
{% load static %}  для подключения внешних статических файлов
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <link type="text/css" href="{% static 'women/css/styles.css' %}" rel="stylesheet" />
    static тег для подключения статических файлов а 'women/css/styles.css' путь к одному файлу их них
</head>
<body>
{% block mainmenu %}   заполняется в соответствующих шаблонах
<ul>
{% for m in menu %}  отражаем список меню из файла views.py
<li>{{m}}</li>
    {% endfor %}
</ul>
{% endblock mainmenu %}

{% block content %} заполняется в соответствующих шаблонах
{% endblock %}
</body>
</html> -->
