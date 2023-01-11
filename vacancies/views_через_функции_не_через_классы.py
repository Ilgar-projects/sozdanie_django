import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from vacancies.models import Vacancy


# 1- создаём вьюшку
def hello(request):  # request это данные которые послал пользователь
    return HttpResponse(
        "керим круто отметил новый год в москве первый раз")  # принимает от пользователя рекуэст и возвращает текст Hello world


# 2- и теперь эту вьюшку нужно обьявить в urls.py
# 3- потом в setting в INSTALLED_APPS в котором имена всех приложений в нашем джанго проекте
# 'vacancies' это записали в setting в INSTALLED_APPS.
@csrf_exempt # отключаем проверку csr с помощью декоратора, импортировав её
# этот декоратор работает только для функций, не для классов
def index(request):
    if request.method == "GET":
        '''запрос от пользователя именно на получение информации,
                 не поиск отдельной инфы из этой информации, а польностью-запрос на вывод всей таблицы,
                 или что именно означает эта строчка кода?'''

        vacancies = Vacancy.objects.all()
        '''это модель, то есть созданная таблица, не в формате json'''

        search_text = request.GET.get("text", None)
        '''пользователь в форму введёт данные для поиска, в данном случае
        вводит "text", это GET-запрос от пользователя'''

        if search_text:
            vacancies = vacancies.filter(text=search_text)
        '''в модели ищет столбец с названием "text"'''

        response = []
        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text
            })
        '''перебор по vacancies, в данный момент vacancies это отфильтрованная модель с одним столбцом.
        а тогда у переменной vacancy какое значение? Что ей присвоено?'''

        # возвращает список респонс в джейсон формате, а чтобы нормально отображалось по русски пишем json_dumps_params={"ensure_ascii": False}
        # но обычно в нормальный читательный формат переводит фронтед
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
        '''возвращает в json формате нашу отфильтрованную табличку '''
    elif request.method == "POST":
        vacancy_data = json.loads(request.body)  # боди это тело запроса, то есть вводимые данные пользователя
        vacancy = Vacancy()  # создали экземпляр класса
        vacancy.text = vacancy_data["text"]  # записываем в поле текст, введённые данные
        vacancy.save()  # сохраняем внесённые данные
        # id не присваиваем, так как присваивается автматичеки при вызове .save()
        return JsonResponse({
                "id": vacancy.id,
                "text": vacancy.text
            })



def get(request, vacancy_id):
    if request.method == "GET":
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        })
