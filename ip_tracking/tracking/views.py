from django.http import HttpResponse
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

# Home page view
def home_view(request):
    return HttpResponse("Welcome to the IP Tracking Security Project!")

# Login view with HTML form + rate limiting
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # For now, we won’t check credentials (dummy test only)
        return HttpResponse(f"Login attempted with username: {username}")
    
    # If GET request, show login form
    return render(request, "login.html")

