from django.shortcuts import render


def about(request):
    template = "about/about.html"
    context = {}
    return render(
        request,
        template,
        context,
    )
