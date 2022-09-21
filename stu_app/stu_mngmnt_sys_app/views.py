from channels.auth import login
from django.http import HttpResponse
from django.shortcuts import render
from stu_mngmnt_sys_app import email_backend
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
        user = email_backend.authenticate(
            request, request.POST.get("email"), request.POST.get("password"))
        if user != None:
            login(user)
            return HttpResponse("Email : "+request.POST.get("email")+" Password : "+request.POST.get("password"))
        else:
            return HttpResponse("Inavlid Login")


# getUserDetails view
def getUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+"Usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please login first")
