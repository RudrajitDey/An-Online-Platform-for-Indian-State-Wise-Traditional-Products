from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
import logging


class CustomErrorMiddleware:
    """Render custom error templates when DEBUG=True.

    This middleware catches Http404, SuspiciousOperation (400) and
    other exceptions and returns the corresponding error template so
    you can preview production-style error pages while developing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            # If a view returned a 404 response object, replace it with template
            if settings.DEBUG and getattr(response, 'status_code', None) == 404:
                return render(request, 'errors/404.html', status=404)

            return response

        except Http404:
            if settings.DEBUG:
                return render(request, 'errors/404.html', status=404)
            raise

        except SuspiciousOperation:
            if settings.DEBUG:
                return render(request, 'errors/400.html', status=400)
            raise

        except Exception as exc:
            # Log the exception and return 500 template in debug
            logging.exception('Unhandled exception in request')
            if settings.DEBUG:
                return render(request, 'errors/500.html', status=500)
            raise
