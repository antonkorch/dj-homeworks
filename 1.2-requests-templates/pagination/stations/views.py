from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from csv import DictReader
from pagination.settings import BUS_STATION_CSV

with open(BUS_STATION_CSV, encoding='utf-8') as csvfile:
    CONTENT = list(DictReader(csvfile))

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = request.GET.get('page', 1)
    paginator = Paginator(CONTENT, 10)
    bus_stations = paginator.get_page(page_number)
    

    context = {
        'bus_stations': bus_stations,
        'page': bus_stations,
    }
    return render(request, 'stations/index.html', context)
