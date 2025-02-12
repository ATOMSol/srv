from django.shortcuts import render

def index(request):
    template = "landing/index.html"
    return render(request,template)


def auth(request):
    template = "auth/signin.html"
    return render(request,template)


def dashboard(request):
    template = "dashboard/dashboard_home.html"
    return render(request,template)