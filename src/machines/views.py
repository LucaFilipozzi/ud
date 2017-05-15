from django.shortcuts import render
from django.http import Http404

import common.models

def all_machines(request):
    context = {"machines": common.models.DebianHost.objects.all()}
    return render(request, 'machines/all.html', context)

def detail(request, machine_name):
    machine = common.models.DebianHost.objects.get(hostname=machine_name)
    if not machine:
        raise Http404("Machine does not exist")
    context = {'machine': machine}
    return render(request, 'machines/details.html', context)

