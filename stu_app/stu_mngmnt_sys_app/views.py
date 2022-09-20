from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Home page


def homePage(request):
    return render(request, "home.html")


# Login page
def showLoginPage(request):
    return render(request, "login_page.html")


# DoLogin view
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        return HttpResponse("Email : "+request.POST.get("email")+" Password : "+request.POST.get("password"))
