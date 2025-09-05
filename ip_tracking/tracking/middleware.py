from .models import RequestLog
import datetime

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        path = request.path

        RequestLog.objects.create(ip_address=ip, path=path, timestamp=datetime.datetime.now())
        return self.get_response(request)
