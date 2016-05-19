from django.conf.urls import url
from django.contrib.auth import views as auth_views
from apps.hello.views import RequestsView, MainPageView, req_json, \
    PersonUpdate, ajax_login


urlpatterns = [url(r'^$', MainPageView.as_view(), name='mainpage'),
               url(r'^requests$', RequestsView.as_view(), name='requests'),
               url(r'^req_json$', req_json, name='ajax_requests'),
               url(r'^edit$', PersonUpdate.as_view(), name='edit'),
               url(r'^ajax_login$', ajax_login, name='ajax_login'),
               url(r'^login$', auth_views.login, {'template_name': 'hello/login.html'},
                   name='login'),
               url(r'^logout$', auth_views.logout, {'next_page': 'mainpage'},
                   name='logout'),
               ]
