1. Basic IP Logging

Objective: Log the IP address, timestamp, and request path of every incoming request.

Implementation:

RequestLog model with ip_address, timestamp, and path.

IPLoggingMiddleware in middleware.py logs every request.

2. IP Blacklisting

Objective: Block requests from blacklisted IPs.

Implementation:

BlockedIP model stores blocked IP addresses.

Middleware checks each request and returns 403 Forbidden if IP is blocked.

block_ip management command allows adding IPs to the blacklist.

3. IP Geolocation Analytics

Objective: Enhance logs with geolocation (country and city).

Implementation:

RequestLog extended with country and city fields.

Middleware uses django-ipgeolocation API to populate location data.

Geolocation results are cached for 24 hours to optimize performance.

4. Rate Limiting by IP

Objective: Prevent abuse and brute force attacks.

Implementation:

Uses django-ratelimit.

Limits:

Authenticated users: 10 requests/minute

Anonymous users: 5 requests/minute

Applied to sensitive views such as login.

5. Anomaly Detection (Celery Task)

Objective: Flag suspicious IPs automatically.

Implementation:

SuspiciousIP model stores flagged IPs (ip_address, reason, flagged_at).

Celery task (flag_suspicious_ips) runs hourly and flags:

IPs with more than 100 requests in the last hour

IPs accessing sensitive paths like /admin or /login

Requires a RequestLog model populated by middleware.

Scheduled via Celery Beat.

Example Celery Beat Schedule:

app.conf.beat_schedule = {
    'flag-suspicious-ips-every-hour': {
        'task': 'ip_tracking.tasks.flag_suspicious_ips',
        'schedule': crontab(minute=0),  # runs every hour
    },
}

Installation

Clone the repository:

git clone https://github.com/<username>/alx-backend-security.git
cd alx-backend-security


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run Celery worker and beat (for anomaly detection):

celery -A myproject worker --loglevel=info
celery -A myproject beat --loglevel=info

Usage

Middleware logs all requests and blocks blacklisted IPs.

Management command to block IPs:

python manage.py block_ip <ip_address>


Rate-limited views protect sensitive endpoints.

Celery task automatically flags suspicious IPs hourly.

Key Models
Model	Fields	Purpose
RequestLog	ip_address, path, timestamp, country, city	Store request details
BlockedIP	ip_address	Store blacklisted IPs
SuspiciousIP	ip_address, reason, flagged_at	Store flagged IPs
Request Flow – IP Tracking Module

Below is a visual representation of how requests are processed and monitored:

          ┌───────────────┐
          │   User/IP     │
          └───────┬───────┘
                  │
                  ▼
         ┌───────────────────┐
         │ Middleware         │
         │ - Logs request     │
         │ - Checks blacklist │
         │ - Adds geolocation │
         └───────┬───────────┘
                 │
                 ▼
         ┌───────────────────┐
         │ RequestLog Model   │
         │ - ip_address       │
         │ - path             │
         │ - timestamp        │
         │ - country/city     │
         └───────┬───────────┘
                 │
                 ▼
      ┌───────────────────────┐
      │ Rate Limiting (views) │
      │ - Prevent abuse       │
      └───────┬───────────────┘
                 │
                 ▼
         ┌───────────────────┐
         │ Celery Task        │
         │ flag_suspicious_ips│
         │ - Checks logs      │
         │ - Flags suspicious │
         │   IPs              │
         └───────┬───────────┘
                 │
                 ▼
         ┌───────────────────┐
         │ SuspiciousIP Model │
         │ - ip_address       │
         │ - reason           │
         │ - flagged_at       │
         └───────────────────┘


✅ This module provides full-stack IP monitoring and security for Django applications, combining logging, blocking, geolocation, rate limiting, and automated anomaly detection.
