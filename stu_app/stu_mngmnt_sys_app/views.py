from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from stu_mngmnt_sys_app.email_backend import EmailBackend
# Create your views here.


# Home page view
def homePage(request):
    return render(request, "home.html")


# Login page view
def showLoginPage(request):
    return render(request, "login_page.html")


# DoLogin view
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackend.authenticate(
            request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            return HttpResponse("Email : "+request.POST.get("email")+" Password : "+request.POST.get("password"))
        else:
            return HttpResponse("Inavlid Login")


# getUserDetails view
def getUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+"Usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please login first")


# Logout view
def logout_user(request):
    logout(request)
    return HttpResponse("/")
