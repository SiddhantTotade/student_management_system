"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from student_management_system import settings
from stu_mngmnt_sys_app import views, hodViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.showLoginPage),
    path('home', views.homePage),
    path('doLogin', views.doLogin),
    path('logout_user', views.logout_user, name="logout"),
    path('logout_ user', views.logout_user),
    path('admin_home', hodViews.admin_home),
    path('add_staff', hodViews.add_staff),
    path('add_staff_save', hodViews.add_staff_save),
    path('add_course', hodViews.add_course),
    path('add_course_save', hodViews.add_course_save),
    path('add_student', hodViews.add_student),
    path('add_student_save', hodViews.add_student_save),
    path('add_subject', hodViews.add_subject),
    path('add_subject_save', hodViews.add_subject_save),
    path('get_user_details', views.getUserDetails),
    path('manage_staff', hodViews.manage_staff),
    path('manage_student', hodViews.manage_student),
    path('manage_course', hodViews.manage_course),
    path('manage_subject', hodViews.manage_subject),
    path('edit_staff/<str:staff_id>', hodViews.edit_staff),
    path('edit_staff_save', hodViews.edit_staff_save),
    path('edit_student/<str:student_id>', hodViews.edit_student),
    path('edit_student_save', hodViews.edit_student_save),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
