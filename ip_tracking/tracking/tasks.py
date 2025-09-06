from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP
from django.db.models import Count

@shared_task
def flag_suspicious_ips():
    """
    Task to flag suspicious IPs based on:
    1. Excessive requests (>100 per hour)
    2. Accessing sensitive paths (/admin, /login)
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1️⃣ Detect high request rate
    request_counts = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(request_count=Count('id'))

    for item in request_counts:
        if item['request_count'] > 100:
            SuspiciousIP.objects.create(
                ip_address=item['ip_address'],
                reason=f"More than 100 requests in the last hour ({item['request_count']})"
            )

    # 2️⃣ Detect access to sensitive paths
    sensitive_paths = ['/admin', '/login']
    suspicious_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    )

    for req in suspicious_requests:
        SuspiciousIP.objects.create(
            ip_address=req.ip_address,
            reason=f"Accessed sensitive path {req.path}"
        )

    return "Suspicious IPs flagged successfully"

