import stripe
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from materials.models import Course, Lesson, Payments, Subscription
from materials.paginators import MaterialsPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from materials.services import StripeService


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='moderator'):
            return Course.objects.all()
        elif not self.request.user.is_staff or not self.request.user.groups.filter(name='moderator'):
            return Lesson.objects.filter(owner=self.request.user)
        else:
            raise PermissionDenied

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='moderator'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='moderator'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='moderator'):
            return Lesson.objects.all()
        elif not self.request.user.is_staff or not self.request.user.groups.filter(name='moderator'):
            return Lesson.objects.filter(owner=self.request.user)
        else:
            raise PermissionDenied


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsModerator]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_of_payment',)
    permission_classes = [IsAuthenticated]


# class CreatePamentAPIView(generics.CreateAPIView):
#     """Эндпоинт для создания платежа"""
#     serializer_class = PaymentsSerializer
#
#     def perform_create(self, serializer):
#         new_payment = serializer.save()
#         new_payment.user = self.request.user
#         lesson_pk = self.kwargs.get('pk')
#         new_payment.paid_lesson = Lesson.objects.get(pk=lesson_pk)
#         session = StripeService('sk_test_51OdpQfDSrjU6WamMGigGvgcd97z7fXogQ8iKnWFd9MtcEl31dO0PflwkThdsEoQTlRokqjbk8a7pTQlaYQ8Wh4Dm00B2axWiqN').create_payment(new_payment.paid_lesson, new_payment.user)
#         new_payment.session_id = session.id
#         new_payment.payment_url = session.url
#         new_payment.save()
#
# class CheckPaymentAPIView(generics.RetrieveAPIView):
#     """Эндпоинт для проверки платежа"""
#     serializer_class = PaymentsSerializer
#     queryset = Payments.objects.all()
#
#     def get_object(self):
#         self.object = super().get_object()
#         session_id = self.object.session_id
#         session = StripeService('sk_test_51OdpQfDSrjU6WamMGigGvgcd97z7fXogQ8iKnWFd9MtcEl31dO0PflwkThdsEoQTlRokqjbk8a7pTQlaYQ8Wh4Dm00B2axWiqN').check_payment(session_id)
#         if session.payment_status == 'paid' or session.payment_status == 'complete':
#             self.object.is_paid = True
#         self.object.save()
#         return self.object

# class PaymentsCreateApiView(generics.CreateAPIView):
#     serializer_class = PaymentsSerializer
#
#     def perform_create(self, serializer):
#         new_lesson = serializer.save()
#         new_lesson.user = self.request.user
#         new_payment = serializer.save()
#         stripe.api_key = 'sk_test_51OdpQfDSrjU6WamMGigGvgcd97z7fXogQ8iKnWFd9MtcEl31dO0PflwkThdsEoQTlRokqjbk8a7pTQlaYQ8Wh4Dm00B2axWiqN'
#         payment_intent = stripe.PaymentIntent.create(
#             amount=2000,
#             currency="usd",
#             automatic_payment_methods={"enabled": True},
#         )
#         new_payment.session_id = payment_intent.id
#         new_payment.amount = payment_intent.amount
#         new_payment.save()
#
#         return super().perform_create(new_payment)
#
#
# class GetPaymentView(APIView):
#
#     def get(self, request, payment_id):
#         payment = Payments.objects.get(pk=payment_id)
#         payment_id = payment.session_id
#         stripe.api_key = 'sk_test_51OdoXSHC8LUh8NqZQboynIwfP7znL7qfNqCOqOYkl7k3pzAKN8QU45ye5RpnABJ2MRjLBfk6tWWisTmY9QoiXJNR00NP3ImbNV'
#         payment_intent = stripe.PaymentIntent.retrieve(payment_id)
#         print(payment_intent)
#         return Response({'status': payment_intent.status, 'body': payment_intent})


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
