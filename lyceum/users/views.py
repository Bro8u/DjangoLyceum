from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import django.http
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import django.urls.exceptions
from django.utils.timezone import now, timedelta

from users.forms import CustomUserForm, ProfileForm, UserForm
from users.models import Profile


__all__ = ["signup", "activate_user", "user_detail", "user_list"]


def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data["username"],
                is_active=django.conf.settings.DEFAULT_USER_IS_ACTIVE,
            )
            user.set_password(form.cleaned_data["password1"])
            user.save()
            Profile.objects.create(user=user, mail=form.cleaned_data["mail"])
            activation_url = reverse("users:activate_user", args=[user.id])
            full_url = f"http://127.0.0.1:8000{activation_url}"
            send_mail(
                "Активируйте ваш аккаунт",
                f"Перейдите по ссылке для активации: {full_url}",
                django.conf.settings.FEEDBACK_SENDER,
                [form.cleaned_data["mail"]],
                fail_silently=False,
            )
            return redirect(
                django.urls.reverse("homepage:homepage"),
            )

        return redirect(
            django.urls.reverse("feedback:feedback"),
        )

    form = CustomUserForm()
    template = "users/signup.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def activate_user(request, user_id):
    user = get_object_or_404(django.contrib.auth.models.User, id=user_id)

    if now() - user.date_joined > timedelta(hours=12):
        return django.http.HttpResponse(
            "Activation link has expired.",
            status=400,
        )

    if user.is_active:
        return django.http.HttpResponse(
            "User is already active.",
            status=400,
        )

    user.is_active = True
    user.save()

    return django.http.HttpResponse("User successfully activated!")


def user_detail(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    template = "users/user_detail.html"
    context = {"profile": profile}
    return render(request, template, context)


@login_required
def user_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(
                django.urls.reverse("users:user_profile"),
            )

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    template = "users/profile.html"
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, template, context)


def user_list(request):
    profiles = Profile.objects.filter(is_active=True)
    template = "users/user_list.html"
    context = {"profiles": profiles}
    return render(request, template, context)
