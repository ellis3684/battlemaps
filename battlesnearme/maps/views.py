from django.shortcuts import render
import os


def home(request):
    maps_key = os.environ.get('MAPS_API_KEY')
    context = {
        'key': maps_key,
    }
    return render(request, 'maps/index.html', context)


def about(request):
    return render(request, 'maps/about.html')
