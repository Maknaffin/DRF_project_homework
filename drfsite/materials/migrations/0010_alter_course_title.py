# Generated by Django 5.0.1 on 2024-01-29 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0009_alter_lesson_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Название курса'),
        ),
    ]
