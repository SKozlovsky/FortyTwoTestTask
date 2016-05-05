from django.conf.urls import url
from apps.hello.views import MainPageView

urlpatterns = [url(r'^$', MainPageView.as_view(), name='mainpage')]
