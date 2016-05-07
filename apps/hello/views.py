
# -*- encoding: utf-8 -*-
import json
from django.views.generic.base import TemplateView
from apps.hello.models import Person, RequestCollect
from django.http import HttpResponse


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
