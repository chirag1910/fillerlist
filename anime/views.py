from django.shortcuts import render, redirect
from anime import api as anime_api
from analytics import api as analytics_api
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from django.conf import settings


def home_page(request):
    if request.method == 'GET':
        context = anime_api.random()
        context.update({
            'show_large_navbar': True,
            'is_home_page': True,
            'anime_json': dumps(context['data'])
        })

        return render(request, "home_page.html", context)
    else:
        return redirect("/404")


def search_page(request):
    if request.method == 'GET':
        keyword = request.GET.get('q')

        if not keyword:
            return redirect("/404")
        else:
            context = anime_api.search(keyword)
            context.update({
                'is_search_page': True,
                'anime_json': dumps(context['data'])
            })

            return render(request, "search_page.html", context)
    else:
        return redirect("/404")


def about_page(request):
    if request.method == 'GET':
        context = {
            'about_page': True
        }

        return render(request, "about_page.html", context)
    else:
        return redirect("/404")


def anime_page(request, id):
    if request.method == 'GET':
        analytics_api.add(request)

        context = anime_api.anime(id)
        context.update({
            'anime_json': dumps(context['data'])
        })

        return render(request, "anime_page.html", context)
    else:
        return redirect("/404")


@csrf_exempt
def update_file(request):
    print("running")
    try:
        if request.method == 'POST':
            key = request.POST.get('key')

            if settings.FILE_UPLOAD_SECRET_KEY and key == settings.FILE_UPLOAD_SECRET_KEY:
                if request.FILES:
                    anime_api.update_data(request.FILES['file'])
                    return JsonResponse({"status": "ok", "message": "File updated successfully"})

                return JsonResponse({"status": "error", "error": "Some error occurred"})

        return redirect("/404")
    except Exception as e:
        print(e)
