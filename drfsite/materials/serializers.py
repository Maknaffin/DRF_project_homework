from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from materials.models import Course, Lesson, Payments, Subscription
from materials.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field="title", queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_count_lessons(self, instance):
        return instance.lessons.all().count()

    def get_subscription(self, instance):
        return Subscription.objects.filter(course=instance, user=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
