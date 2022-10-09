import json
from django.urls import reverse
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from stu_mngmnt_sys_app.email_backend import EmailBackend
from django.contrib import messages
import requests
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
        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6Le6qWciAAAAAIRE6OikFzTG_YZsliwfOlDu3OHq"
        captcha_data = {'secret':captcha_secret,'response':captcha_token}
        captcha_server_response = requests.post(url=captcha_url,data=captcha_data)
        captcha_json = json.loads(captcha_server_response.text)
        if captcha_json['success'] == False:
            messages.error(request, "Invalid captcha. Try again")
            return HttpResponseRedirect("/")
        user = EmailBackend.authenticate(
            request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid login details")
            return HttpResponseRedirect("/")


# getUserDetails view
def getUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+"Usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please login first")


# Logout view
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


# Firebase view
def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js")' \
        'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js")' \
        'var firebaseConfig = {' \
        'apiKey: "AIzaSyAYA_vrqh0lZwYddKCmpz3wtjxHAzklymw",' \
        'authDomain: "mystudentmanagementsystem.firebaseapp.com",' \
        'projectId: "mystudentmanagementsystem",' \
        'storageBucket: "mystudentmanagementsystem.appspot.com",' \
        'messagingSenderId: "387678679441",' \
        'appId: "1:387678679441:web:73496e301d0e7f533b2a30",' \
        'measurementId: "G-Y8RXSLPSQZ"' \
        '};' \
        'fireabse.initializeApp(firebaseConfig)'\
        'const messaging = firebase.messaging()' \
        'messaging.setBackgroundMessagingHandler(function(payload) { ' \
        'console.log(payload)' \
        'const notification=JSON.parse(payload)' \
        'const notificationOption={' \
        '    body: notification.body,' \
        '    icon: notification.icon' \
        '}'\
        'return self.registration.showNotification(payload.notification.title, notificationOption)'\
        '});'

    return HttpResponse(data,content_type="text/javascript")
