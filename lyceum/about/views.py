from django.shortcuts import render

__all__ = ["about"]


def about(request):
    template = "about/about.html"
    context = {}
    return render(
        request,
        template,
        context,
    )
