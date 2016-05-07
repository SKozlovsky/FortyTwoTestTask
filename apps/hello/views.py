# -*- encoding: utf-8 -*-
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    template_name = "hello/hc.html"
