from django.urls import path, re_path, register_converter
from catalog import converters, views

register_converter(converters.DigitConverter, "custom_converter")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:id>/", views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<number>[1-9]\d*)/$",
        views.reqular_expression,
        name="reqular_expression",
    ),
    path(
        "converter/<custom_converter:number>/",
        views.converter,
        name="converter",
    ),
]
