from django.conf import settings
from django.db import models
from users.models import NULLABLE, User

PAY_CARD = 'card'
PAY_CASH = 'cash'

PAY_TYPES = (
    (PAY_CASH, 'наличные'),
    (PAY_CARD, 'перевод')
)


class Course(models.Model):
    title = models.CharField(max_length=250, **NULLABLE, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=250, **NULLABLE, verbose_name='Название урока')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    link_to_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE,
                               related_name="lessons")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, **NULLABLE)
    date_of_payment = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(Course, verbose_name='Оплаченный курс', on_delete=models.CASCADE, **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, verbose_name='Оплаченный урок', on_delete=models.CASCADE, **NULLABLE)
    payment_sum = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=10, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.date_of_payment}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.sub_course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
