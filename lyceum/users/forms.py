from django import forms
from django.contrib.auth.models import User

from users.models import Profile


class CustomUserForm(forms.ModelForm):
    mail = forms.EmailField(
        label="Эл. почта",
        help_text="Введите ваш email.",
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Придумайте пароль.",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Повторите пароль.",
    )

    class Meta:
        model = User
        fields = [User.username.field.name]
        labels = {
            User.username.field.name: "Имя пользователя",
        }
        help_texts = {
            User.username.field.name: "Придумайте имя для входа.",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return password2


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]
        labels = {
            "first_name": "Имя",
        }
        help_texts = {
            "first_name": "Введите ваше имя.",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["mail", "birthday", "image"]
        labels = {
            "mail": "Почта",
            "birthday": "День рождения",
            "image": "Картинка",
        }
        help_texts = {
            "mail": "Введите вашу почту.",
            "birthday": "Выберите дату рождения.",
            "image": "Загрузите изображение профиля.",
        }
