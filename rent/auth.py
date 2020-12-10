from django.http import request, HttpResponse
from django.shortcuts import render
from django.template import loader

from . import models
from . import Controller


class auth:
    def __init__(self):
        if 'user' not in request.session:
            template = loader.get_template('auth/login.html')
            return HttpResponse(template.render({}, request))
        else:
            # print(request.session['user'])
            template = loader.get_template('clerk/view-catalog.html')
            return HttpResponse(template.render({}, request))