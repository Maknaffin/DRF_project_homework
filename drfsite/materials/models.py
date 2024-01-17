from django.db import models
from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название урока')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    link_to_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE, related_name="lessons")

    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
