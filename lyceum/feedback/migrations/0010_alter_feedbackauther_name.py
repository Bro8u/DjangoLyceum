# Generated by Django 4.2.14 on 2024-11-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0009_remove_feedback_created_feedback_created_on"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackauther",
            name="name",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Имя"
            ),
        ),
    ]
