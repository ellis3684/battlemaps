from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from .battle_finder import BattleFinder
import os

to_email = os.environ.get('ADMIN_TO_EMAIL')


def get_battles(request, latitude, longitude, iteration):
    user_latitude = latitude
    user_longitude = longitude
    list_end = int(iteration) * 10
    list_start = list_end - 10
    try:
        finder = BattleFinder(user_latitude, user_longitude)
    except ValueError:
        return HttpResponseNotFound("That is not a valid latitude/longitude.")
    else:
        nearest_battles = finder.get_nearest_battles(list_start, list_end)
        return JsonResponse(nearest_battles, safe=False)


def add_battle(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                subject = 'New request submitted for Battle Maps'
                battle_name = form.cleaned_data['battle_name']
                battle_link = form.cleaned_data['battle_link']
                battle_date = form.cleaned_data['battle_date']
                battle_latitude = form.cleaned_data['battle_latitude']
                battle_longitude = form.cleaned_data['battle_longitude']
                user_message = form.cleaned_data['message']
                from_email = form.cleaned_data['user_email']
                message = f'Request comes from: {from_email}\n' \
                          f'Battle Name: {battle_name}\n' \
                          f'Battle Link: {battle_link}\n' \
                          f'Battle Date: {battle_date}\n' \
                          f'Latitude: {battle_latitude}\n' \
                          f'Longitude: {battle_longitude}\n' \
                          f'Message: {user_message}'
                send_mail(subject, message, from_email, [to_email])
            except BadHeaderError:
                messages.warning(request, 'Invalid header found. Your request was not successfully submitted.')
                return redirect('add-battle')
            messages.success(request, 'Your request has been successfully submitted.')
            return redirect('add-battle')
    else:
        form = ContactForm()
    return render(request, 'maps/add-battle.html', {'form': form})
