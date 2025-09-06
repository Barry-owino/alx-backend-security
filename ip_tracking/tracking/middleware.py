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

class GeoLocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        cache_key = f"geo_{ip}"

        # Check if we already cached location
        location = cache.get(cache_key)
        if not location:
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/")  # Free API
                data = response.json()
                location = {
                    "country": data.get("country_name", "Unknown"),
                    "city": data.get("city", "Unknown")
                }
                # Cache for 24 hours
                cache.set(cache_key, location, 60 * 60 * 24)
            except Exception:
                location = {"country": "Unknown", "city": "Unknown"}

        # Update the latest RequestLog for this IP and path
        RequestLog.objects.filter(ip_address=ip).order_by('-timestamp').first() \
            .update(country=location["country"], city=location["city"])

        return self.get_response(request)
