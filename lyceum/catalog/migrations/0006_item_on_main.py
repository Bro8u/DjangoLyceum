# Generated by Django 4.2.14 on 2024-11-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_mainimage_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="on_main",
            field=models.BooleanField(default=True),
        ),
    ]
