from django.db import models


class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта")
    ]

    slug = models.SlugField(max_length=50)  # slug нужен для красивого отображения url
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    # created = models.DateField(auto_now_add=True)  # auto_now_add=True поставить текущее значение в момент создания

    # создастся дата создания вакансии

    # при любых изменениях в моделях нужно делать миграцию
    # в терминале прописать python manage.py makemigrations потом python manage.py migrate
    def __str__(self):
        return self.slug


a = Vacancy()

