from django.contrib.auth import views as auth_views
from django.urls import path

import users.views


app_name = "users"


auth_views_with_templates = [
    ("login/", auth_views.LoginView, "users/login.html", "login"),
    ("logout/", auth_views.LogoutView, "users/logout.html", "logout"),
    (
        "password_change/",
        auth_views.PasswordChangeView,
        "users/password_change.html",
        "password_change",
    ),
    (
        "password_change/done/",
        auth_views.PasswordChangeDoneView,
        "users/password_change_done.html",
        "password_change_done",
    ),
    (
        "password_reset/",
        auth_views.PasswordResetView,
        "users/password_reset.html",
        "password_reset",
    ),
    (
        "password_reset/done/",
        auth_views.PasswordResetDoneView,
        "users/password_reset_done.html",
        "password_reset_done",
    ),
    (
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView,
        "users/password_reset_confirm.html",
        "password_reset_confirm",
    ),
    (
        "reset/done/",
        auth_views.PasswordResetCompleteView,
        "users/password_reset_complete.html",
        "password_reset_complete",
    ),
]

auth_urlpatterns = []
for url_pat, view_class, template_name, name in auth_views_with_templates:
    auth_urlpatterns.append(
        path(
            url_pat,
            view_class.as_view(template_name=template_name),
            name=name,
        ),
    )

users_urlpatterns = [
    path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
    path(
        "activate/<int:user_id>/",
        users.views.activate_user,
        name="activate_user",
    ),
    path(
        "profile/",
        users.views.user_profile,
        name="user_profile",
    ),
    path(
        "user_detail/<int:user_id>/",
        users.views.user_detail,
        name="user_detail",
    ),
    path(
        "user_list/",
        users.views.user_list,
        name="user_list",
    ),
]

urlpatterns = users_urlpatterns + auth_urlpatterns
