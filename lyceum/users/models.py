from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    mail = models.EmailField(
        "почта",
    )
    birthday = models.DateField(
        "дата рождения",
        default="2000-01-01",
        # blank=True,
        # null=True,
    )
    coffe_count = models.PositiveIntegerField(
        "чашки кофе",
        default=0,
    )
    image = models.ImageField(
        "изображение",
        upload_to=image_path,
        # null=True,
        # blank=True,
    )
