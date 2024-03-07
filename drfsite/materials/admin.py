from django.contrib import admin

from materials.models import Payments, Lesson, Course, Subscription

admin.site.register(Payments)

admin.site.register(Lesson)

admin.site.register(Course)

admin.site.register(Subscription)
