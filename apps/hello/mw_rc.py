# -*- encoding: utf-8 -*-
from apps.hello.models import RequestCollect


class MiddlewareRC(object):

    def process_response(self, request, response):
        if request.is_ajax():
            return response

        RequestCollect.objects.create(r_path=request.path,
                                      r_method=request.method,
                                      r_status=response.status_code)
        if request.path == '/requests':
            RequestCollect.objects.all().update(r_viewed=True)

        return response
