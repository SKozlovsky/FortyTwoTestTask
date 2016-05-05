# -*- encoding: utf-8 -*-
from django.views.generic.base import TemplateView
from apps.hello.models import Person


class MainPageView(TemplateView):

    template_name = "hello/mainpage.html"

    def get_context_data(self, **kwargs):

        context = super(MainPageView, self).get_context_data(**kwargs)
        context['title'] = 'Hello'
        context['object'] = Person.objects.first()

        return context
