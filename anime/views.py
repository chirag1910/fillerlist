from django.shortcuts import render, redirect
from anime import api as anime_api
from analytics import api as analytics_api
from json import dumps


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


def anime_page(request, slug):
    if request.method == 'GET':
        analytics_api.add(request)

        context = anime_api.anime(slug)
        context.update({
            'anime_json': dumps(context['data'])
        })

        return render(request, "anime_page.html", context)
    else:
        return redirect("/404")
