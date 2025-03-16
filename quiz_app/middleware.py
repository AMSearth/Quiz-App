import sys
import traceback
import logging
from django.http import HttpResponse
from django.conf import settings

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Log the full traceback
            exc_info = sys.exc_info()
            logger.error(
                f"Unhandled exception: {str(e)}\n"
                f"Request path: {request.path}\n"
                f"Request method: {request.method}\n"
                f"Request data: {request.POST if request.method == 'POST' else request.GET}\n"
                f"Traceback: {''.join(traceback.format_exception(*exc_info))}"
            )
            
            # In debug mode, re-raise the exception
            if settings.DEBUG:
                raise
            
            # In production, return a 500 response
            return HttpResponse(
                "An unexpected error occurred. The error has been logged and will be addressed.",
                status=500
            ) 