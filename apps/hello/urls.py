from django.conf.urls import url
from apps.hello.views import RequestsView, MainPageView, req_json
from django.views.generic.base import TemplateView


urlpatterns = [url(r'^$', MainPageView.as_view(), name='mainpage'),
               url(r'^requests$', RequestsView.as_view(), name='requests'),
               url(r'^req_json$', req_json, name='ajax_requests'),
               url(r'^edit$', TemplateView.as_view(template_name="hello/hc_edit.html")),
               ]
