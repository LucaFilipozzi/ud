from django.http import HttpResponse
from django.shortcuts import render


def all_machines(request):
    context = {}
    return render(request, 'machines/all.html', context)

def detail(request, machine_name):
    context = {'name': machine_name}
    return render(request, 'machines/details.html', context)

