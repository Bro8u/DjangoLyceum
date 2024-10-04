from django.http import HttpResponse


def catalog(request):
    return HttpResponse("Welcome to the catalog page!")
