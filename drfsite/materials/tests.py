from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            course=self.course,
            owner=self.user,
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            'title': self.lesson,
            'course': self.course,
            'link_to_video': 'https://www.youtube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs'
        }
        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_lesson(self):
        """Тестирование списка уроков"""
        response = self.client.get(
            reverse('materials:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(
            reverse('materials:lesson-get', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        """Тестирование редактирования уроков"""
        data = {
            'title': 'Test update title',
            'description': 'Test update description',
            'course': self.course,
            'link_to_video': 'https://www.youtube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs'
        }
        response = self.client.put(
            reverse('materials:lesson-update', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_destroy_lesson(self):
        """Тестирование удаления уроков"""
        response = self.client.delete(
            reverse('materials:lesson-delete', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        pass


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_create_subscription(self):
        """Тестирование создания подписки"""

        data = {
            'user': self.user.id,
            'course': self.course.id,
        }
        response = self.client.post(
            reverse('materials:subscription-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_subscription(self):
        """Тестирование списка подписок"""
        response = self.client.get(
            reverse('materials:subscription-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_destroy_subscription(self):
        """Тестирование удаления подписок"""
        response = self.client.delete(
            reverse('materials:subscription-delete', args=[self.subscription.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
    def tearDown(self):
        pass
