from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


__all__ = [
    "CustomUserForm",
    "UserForm",
    "CustomUserCreationForm",
    "CustomUserChangeForm",
]


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
        fields = [User.first_name.field.name]
        labels = {
            User.first_name.field.name: "Имя",
        }
        help_texts = {
            User.first_name.field.name: "Введите ваше имя.",
        }


class ProfileForm(forms.ModelForm):
    coffee_count = forms.IntegerField(
        label="Количество выпитого кофе",
        required=False,
        disabled=True,
        help_text="Ради кофе можно",
    )

    class Meta:
        model = Profile
        fields = [
            Profile.mail.field.name,
            Profile.birthday.field.name,
            Profile.image.field.name,
            Profile.coffee_count.field.name,
        ]
        labels = {
            Profile.mail.field.name: "Почта",
            Profile.birthday.field.name: "День рождения",
            Profile.image.field.name: "Картинка",
            Profile.coffee_count.field.name: "Количество выпитого кофе",
        }
        help_texts = {
            Profile.mail.field.name: "Введите вашу почту.",
            Profile.birthday.field.name: "Выберите дату рождения.",
            Profile.image.field.name: "Загрузите изображение профиля.",
            Profile.coffee_count.field.name: "Ради кофе можно",
        }


class CustomUserCreationForm(UserCreationForm):
    mail = forms.EmailField(
        label=Profile.mail.field.verbose_name,
        help_text=Profile.mail.field.help_text or "Введите ваш email.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            User.username.field.name,
            Profile.mail.field.name,
            User.password.field.name + "1",  # password1
            User.password.field.name + "2",  # password2
        ]
        labels = {
            User.username.field.name: User.username.field.verbose_name,
            Profile.mail.field.name: Profile.mail.field.verbose_name,
        }
        help_texts = {
            User.username.field.name: User.username.field.help_text,
        }


class CustomUserChangeForm(UserChangeForm):
    coffee_count = forms.IntegerField(
        label=Profile.coffee_count.field.verbose_name,
        required=False,
        help_text=Profile.coffee_count.field.help_text
        or "Количество чашек кофе",
        disabled=True,
    )

    birthday = forms.DateField(
        label=Profile.birthday.field.verbose_name,
        required=False,
        help_text=Profile.birthday.field.help_text
        or "Выберите дату рождения.",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta(UserChangeForm.Meta):
        model = Profile
        fields = [
            Profile.mail.field.name,
            Profile.birthday.field.name,
            Profile.coffee_count.field.name,
        ]
        labels = {
            Profile.mail.field.name: "Эл. почта",
            Profile.birthday.field.name: "День рождения",
            Profile.coffee_count.field.name: "Количество выпитого кофе",
        }
        help_texts = {
            User.username.field.name: "Ваше имя пользователя.",
            Profile.mail.field.name: "Ваше имя пользователя.",
            Profile.birthday.field.name: "Ваше имя пользователя.",
            Profile.coffee_count.field.name: "Ради кофе можно",
        }
