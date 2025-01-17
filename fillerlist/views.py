from django.shortcuts import render


def error_page(request, exception=None):
    return render(request, "error_page.html")
