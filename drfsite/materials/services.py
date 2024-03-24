import stripe

import smtplib

from django.core.mail import send_mail

# from config.settings import EMAIL_HOST_USER


class StripeService:
    """Класс для сервиса stripe"""

    def __init__(self, api_key):
        self.api_key = api_key

    def create_payment(self, obj, user):
        """Метод создания сессии платежа"""
        stripe.api_key = self.api_key
        create_product = stripe.Product.create(
            name=obj.title,
        )

        price = stripe.Price.create(
            unit_amount=int(obj.amount) * 100,
            currency='rub',
            product=create_product['id'],
        )

        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1
                }
            ],
            mode="payment",
            client_reference_id=user.id
        )
        return session

    def check_payment(self, session_id):
        """Метод проверки платежа"""
        stripe.api_key = self.api_key

        session = stripe.checkout.Session.retrieve(session_id)

        return session


def send_mailing(client_list, subject, body):
    """Функция отправки письма"""
    try:
        response = send_mail(
            subject,
            body,
            EMAIL_HOST_USER,
            client_list
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException