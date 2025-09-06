from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import datetime

class BlockedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        #check if ip is in blocklist
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")
        return self.get_response(request)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        path = request.path

        RequestLog.objects.create(ip_address=ip, path=path, timestamp=datetime.datetime.now())
        return self.get_response(request)
