from django.http import HttpResponse
from django.shortcuts import render


def farming_home_view(request):
    return HttpResponse("Hello, this is the Farming app home page")
