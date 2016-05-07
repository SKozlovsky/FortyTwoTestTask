from django.conf.urls import url
from apps.hello.views import RequestsView, MainPageView, req_json


urlpatterns = [url(r'^$', MainPageView.as_view(), name='mainpage'),
               url(r'^requests$', RequestsView.as_view(), name='requests'),
               url(r'^req_json$', req_json, name='ajax_requests'),
               ]
