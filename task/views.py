from django.http import HttpResponse
from django.shortcuts import render


def task_home_view(request):
    return HttpResponse("hello, from the Task app home page")
