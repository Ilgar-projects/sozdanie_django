import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


# 1- создаём вьюшку
def hello(request):  # request это данные которые послал пользователь
    return HttpResponse(
        "hello world")  # принимает от пользователя рекуэст и возвращает текст Hello world


# 2- и теперь эту вьюшку нужно обьявить в urls.py
# 3- потом в setting в INSTALLED_APPS в котором имена всех приложений в нашем джанго проекте
# 'vacancies' это записали в setting в INSTALLED_APPS.

@method_decorator(csrf_exempt, name="dispatch")
class VacancyView(View):
    def get(self, request):
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

    def post(self, request):
        vacancy_data = json.loads(request.body)  # боди это тело запроса, то есть вводимые данные пользователя
        vacancy = Vacancy()  # создали экземпляр класса
        vacancy.text = vacancy_data["text"]  # записываем в поле текст, введённые данные
        vacancy.save()  # сохраняем внесённые данные
        # id не присваиваем, так как присваивается автматичеки при вызове .save()
        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        })


# специальный класс для детального отображения элемента DetaiView
# в данном случае отображение определённой вакансии
@method_decorator(csrf_exempt, name="dispatch")
class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()  # метод get_object возвращает наш элемент

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        })
