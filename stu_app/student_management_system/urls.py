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

from django.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from student_management_system import settings
from stu_mngmnt_sys_app import views, hodViews, studentViews, staffViews
from stu_mngmnt_sys_app.editResultViewClass import EditResultViewClass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # HOD url path
    path('', views.showLoginPage, name="show_login"),
    path('home', views.homePage),
    path('doLogin', views.doLogin, name="do_login"),
    path('logout_user', views.logout_user, name="logout"),
    path('admin_home', hodViews.admin_home, name="admin_home"),
    path('add_staff', hodViews.add_staff, name="add_staff"),
    path('add_staff_save', hodViews.add_staff_save, name="add_staff_save"),
    path('add_course', hodViews.add_course, name="add_course"),
    path('add_course_save', hodViews.add_course_save, name="add_course_save"),
    path('add_student', hodViews.add_student, name="add_student"),
    path('add_student_save', hodViews.add_student_save, name="add_student_save"),
    path('add_subject', hodViews.add_subject, name="add_subject"),
    path('add_subject_save', hodViews.add_subject_save, name="add_subject_save"),
    path('get_user_details', views.getUserDetails, name="get_user_details"),
    path('manage_staff', hodViews.manage_staff, name="manage_staff"),
    path('manage_student', hodViews.manage_student, name="manage_student"),
    path('manage_course', hodViews.manage_course, name="manage_course"),
    path('manage_subject', hodViews.manage_subject, name="manage_subject"),
    path('edit_staff/<str:staff_id>', hodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', hodViews.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>',
         hodViews.edit_student, name="edit_student"),
    path('edit_student_save', hodViews.edit_student_save, name="edit_student_save"),
    path('edit_subject/<str:subject_id>',
         hodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save', hodViews.edit_subject_save, name="edit_subject_save"),
    path('edit_course/<str:course_id>', hodViews.edit_course, name="edit_course"),
    path('edit_course_save', hodViews.edit_course_save, name="edit_course_save"),
    path('add_session_save', hodViews.add_session_save, name="add_session_save"),
    path('manage_session', hodViews.manage_session, name="manage_session"),
    path('check_email_exist', hodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', hodViews.check_username_exist,
         name="check_username_exist"),
    path('student_feedback_message', hodViews.student_feedback_message,
         name="student_feedback_message"),
    path('student_feedback_message_replied', hodViews.student_feedback_message_replied,
         name="student_feedback_message_replied"),
    path('staff_feedback_message', hodViews.staff_feedback_message,
         name="staff_feedback_message"),
    path('staff_feedback_message_replied', hodViews.staff_feedback_message_replied,
         name="staff_feedback_message_replied"),
    path('student_leave_view', hodViews.student_leave_view,
         name="student_leave_view"),
    path('staff_leave_view', hodViews.staff_leave_view, name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>',
         hodViews.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>',
         hodViews.student_disapprove_leave, name="student_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>',
         hodViews.staff_approve_leave, name="staff_approve_leave"),
    path('staff_disapprove_leave/<str:leave_id>',
         hodViews.staff_disapprove_leave, name="staff_disapprove_leave"),
    path('admin_view_attendance', hodViews.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_date', hodViews.admin_get_attendance_date,
         name="admin_get_attendance_date"),
    path('admin_get_attendance_student', hodViews.admin_get_attendance_student,
         name="admin_get_attendance_student"),
    path('admin_profile', hodViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', hodViews.admin_profile_save,
         name="admin_profile_save"),
    path('admin_send_notification_staff', hodViews.admin_send_notification_staff,
         name="admin_send_notification_staff"),
    path('admin_send_notification_student', hodViews.admin_send_notification_student,
         name="admin_send_notification_student"),
    path('send_student_notification', hodViews.send_student_notification,
         name="send_student_notification"),
    path('send_staff_notification', hodViews.send_staff_notification,
         name="send_staff_notification"),

    # Staff url path
    path('staff_home', staffViews.staff_home, name="staff_home"),
    path('get_students', staffViews.get_students, name="get_students"),
    path('staff_take_attendance', staffViews.staff_take_attendance,
         name="staff_take_attendance"),
    path('staff_update_attendance', staffViews.staff_update_attendance,
         name="staff_update_attendance"),
    path('save_attendance_data', staffViews.save_attendance_data,
         name="save_attendance_data"),
    path('save_updateattendance_data', staffViews.save_updateattendance_data,
         name="save_updateattendance_data"),
    path('get_attendance_date', staffViews.get_attendance_date,
         name="get_attendance_date"),
    path('get_attendance_student', staffViews.get_attendance_student,
         name="get_attendance_student"),
    path('staff_apply_leave', staffViews.staff_apply_leave,
         name="staff_apply_leave"),
    path('staff_apply_leave_save', staffViews.staff_apply_leave_save,
         name="staff_apply_leave_save"),
    path('staff_feedback', staffViews.staff_feedback,
         name="staff_feedback"),
    path('staff_feedback_save', staffViews.staff_feedback_save,
         name="staff_feedback_save"),
    path('staff_feedback_save', staffViews.staff_feedback_save,
         name="staff_feedback_save"),
    path('staff_profile', staffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', staffViews.staff_profile_save,
         name="staff_profile_save"),
    path('staff_fcmtoken_save', staffViews.staff_fcmtoken_save,
         name="staff_fcmtoken_save"),
    path('staff_all_notification', staffViews.staff_all_notification,
         name="staff_all_notification"),
    path('staff_add_result', staffViews.staff_add_result,
         name="staff_add_result"),
    path('save_student_result', staffViews.save_student_result,
         name="save_student_result"),
    path('edit_student_result',EditResultViewClass.as_view() ,
         name="edit_student_result"),
    path('fetch_result_student',staffViews.fetch_result_student ,
         name="fetch_result_student"),


    # Student url path
    path('student_home', studentViews.student_home, name="student_home"),
    path('student_view_attendance', studentViews.student_view_attendance,
         name="student_view_attendance"),
    path('student_view_attendance_post', studentViews.student_view_attendance_post,
         name="student_view_attendance_post"),
    path('student_apply_leave', studentViews.student_apply_leave,
         name="student_apply_leave"),
    path('student_apply_leave_save', studentViews.student_apply_leave_save,
         name="student_apply_leave_save"),
    path('student_feedback', studentViews.student_feedback,
         name="student_feedback"),
    path('student_feedback_save', studentViews.student_feedback_save,
         name="student_feedback_save"),
    path('student_profile', studentViews.student_profile, name="student_profile"),
    path('student_profile_save', studentViews.student_profile_save,
         name="student_profile_save"),
    path('student_fcmtoken_save', studentViews.student_fcmtoken_save,
         name="student_fcmtoken_save"),
    path('student_all_notification', studentViews.student_all_notification,
         name="student_all_notification"),
     
    # Firebase path  
    path('firebase-mesaging-sw.js', views.showFirebaseJS,
         name="show_firebase_js"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
