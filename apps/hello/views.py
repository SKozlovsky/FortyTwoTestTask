# -*- encoding: utf-8 -*-
import json
from django.views.generic.base import TemplateView
from apps.hello.models import Person, RequestCollect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.generic.edit import UpdateView
from apps.hello.forms import LoginForm, EditForm
from django.contrib import auth
from django.shortcuts import render_to_response, HttpResponseRedirect

import time


class MainPageView(TemplateView):

    template_name = "hello/mainpage.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['title'] = 'Hello'
        context['object'] = Person.objects.first()
        return context


class RequestsView(TemplateView):

    template_name = "hello/requests.html"

    def get_context_data(self, **kwargs):
        rlist = RequestCollect.objects.order_by('-r_time')[:10]
        context = super(RequestsView, self).get_context_data(**kwargs)
        context['title'] = 'Requests'
        context['requests_list'] = rlist
        return context


def req_json(request):

    undread_requests = RequestCollect.objects.filter(r_viewed=False)

    if 'window_state' in request.GET.keys():
        if request.GET['window_state'] == 'active':
            undread_requests.update(r_viewed=True)
    new_title = "(%i)Requests" % (len(undread_requests))
    response_data = {}
    rlist = RequestCollect.objects.order_by('-r_time')[:10]
    html_rlist = ""
    for req in rlist:
        html_rlist += "<p>%s</p>" % req

    response_data['new_title'] = new_title
    response_data['new_requests_list'] = html_rlist
    response = HttpResponse(json.dumps(response_data),
                            content_type="application/json")
    return response


class PersonUpdate(UpdateView):
    model = Person
    template_name = "hello/edit.html"
    form_class = EditForm
    success_url = '/'

    def get_object(self):
        self.obj = Person.objects.first()
        return self.obj

    def get_context_data(self, **kwargs):
        context = super(PersonUpdate, self).get_context_data(**kwargs)
        context['title'] = 'edit'
        context['object'] = self.obj
        context['login_form'] = LoginForm
        return context

    def form_valid(self, form):
        response = super(PersonUpdate, self).form_valid(form)

        if self.request.is_ajax():
            response_data = {'succses': True}
            response_data["photo"] = "/static/uploads/%s?nocashe=%s" % \
                                     (self.obj.photo, str(time.time()))
            response = HttpResponse(json.dumps(response_data),
                                    content_type="application/json")
        return response

    def form_invalid(self, form):
        response = super(PersonUpdate, self).form_invalid(form)

        if self.request.is_ajax():
            # print dir(form)
            if form.errors:
                errors = form.errors
                print errors
                for (field, error) in form.errors.iteritems():
                    print 'field ', field, 'error  ',  form.errors.get(field)
                print dir(form.errors)
                # print form.errors.iteritems()
                # print type(form.errors.iteritems())
            response_data = {'succses': False, 'errors': form.errors.__str__()}
            response = HttpResponse(json.dumps(response_data),
                                    content_type="application/json")
        return response


def ajax_login(request):
    if request.is_ajax() and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response_data = {'succses': True, 'user': username}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {'succses': False}
            response_data['error'] = 'Username or Password incorrect'
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")

    return HttpResponseRedirect('/login')