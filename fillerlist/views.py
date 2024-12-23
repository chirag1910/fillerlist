from django.shortcuts import render
from . import api
from . import analytics_api
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps


def home_page(request):
    context = api.random()
    context.update({
        'show_large_navbar': True,
        'is_home_page': True,
        'anime_json': dumps(context['data'])
    })

    return render(request, "home_page.html", context)


def search_page(request):
    if request.method == 'GET':
        keyword = request.GET.get('q')
        if not keyword:
            return error_page(request)
        else:
            context = api.search(keyword)
            context.update({
                'is_search_page': True,
                'anime_json': dumps(context['data'])
            })

            return render(request, "search_page.html", context)
    else:
        return error_page(request)


def about_page(request):
    context = {
        'about_page': True
    }
    return render(request, "about_page.html", context)


def anime_page(request, id):
    analytics_api.add(request)
    context = api.anime(id)
    context.update({
        'anime_json': dumps(context['data'])
    })

    return render(request, "anime_page.html", context)


def error_page(request, exception=None):
    return render(request, "error_page.html")


@csrf_exempt
def update_file(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        if key == "tX3rO7qO6vN4oP6":
            if request.FILES:
                api.update_data(request.FILES['file'])
                return JsonResponse({"status": "ok", "message": "File updated successfully"})

            return JsonResponse({"status": "error", "error": "Some error occurred"})

    return error_page(request)


def analytics_page(request):
    context = analytics_api.get()
    return render(request, 'analytics_page.html', context)
