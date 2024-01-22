from django.core.management import BaseCommand

from materials.models import Course, Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {
                "user": None,
                "date_of_payment": "2023-11-23",
                "paid_course": Course.objects.get(title="Puthon-разработчик"),
                "paid_lesson": None,
                "payment_sum": 145000,
                "payment_method": "перевод"
            },
            {
                "user": None,
                "date_of_payment": "2023-11-29",
                "paid_course": Course.objects.get(title="Puthon-разработчик"),
                "paid_lesson": None,
                "payment_sum": 120000,
                "payment_method": "перевод"
            },
            {
                "user": None,
                "date_of_payment": "2023-12-10",
                "paid_course": Course.objects.get(title="Puthon-разработчик"),
                "paid_lesson": None,
                "payment_sum": 155000,
                "payment_method": "перевод"
            },
            {
                "user": None,
                "date_of_payment": "2023-12-31",
                "paid_course": Course.objects.get(title="Puthon-разработчик"),
                "paid_lesson": None,
                "payment_sum": 130000,
                "payment_method": "перевод"
            },
        ]

        payments_for_create = []
        for payment_item in payment_list:
            payments_for_create.append(Payments(**payment_item))

        Payments.objects.all().delete()
        Payments.objects.bulk_create(payments_for_create)