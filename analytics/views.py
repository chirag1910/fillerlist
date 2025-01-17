from django.shortcuts import render
from analytics import api

def analytics_page(request):
    context = api.get()
    return render(request, 'analytics_page.html', context)
