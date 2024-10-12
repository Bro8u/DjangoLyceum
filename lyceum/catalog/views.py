from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, id):
    return HttpResponse(f"<body>Подробно элемент {id}</body>")


def reqular_expression(request, number):
    if number == 0:
        raise ValueError("Только нули")
    return HttpResponse(number)


def converter(request, number):
    return HttpResponse(number)
