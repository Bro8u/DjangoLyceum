from django.contrib.auth.models import User
from django.db import models


__all__ = ["Profile"]


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
    )
    coffee_count = models.PositiveIntegerField(
        "чашки кофе",
        default=0,
    )
    image = models.ImageField(
        "изображение",
        upload_to=image_path,
    )
