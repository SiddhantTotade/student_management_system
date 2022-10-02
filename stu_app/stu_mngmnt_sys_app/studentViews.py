import datetime
from django.shortcuts import render
from .models import Students, Subjects, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, FeedbackStudent
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Rendering student home page
def student_home(request):
    return render(request, "student_template/student_home_template.html")


# Rendering view attendance page
def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {'subjects': subjects})


# Student view attendance
def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_data_parse = datetime.datetime.strptime(
        start_date, "%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    subject_obj = Subjects.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(
        start_data_parse, end_data_parse), subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(
        attendance_id__in=attendance, student_id=stud_obj)

    return render(request, "student_template/student_attendance_data.html", {'attendance_reports': attendance_reports})


# Rendering staff_leave page
def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_apply_leave.html", {'leave_data': leave_data})


# Saving staff leave
def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")
        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(
                student_id=student_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully applied for leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed to applied for leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


# Rendering staff_feedback page
def student_feedback(request):
    student_id = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id=student_id)
    return render(request, "student_template/student_feedback.html", {'feedback_data': feedback_data})


# Saving staff feedback
def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedbackStudent(
                student_id=student_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Thankyou for feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Feedback submission failed")
            return HttpResponseRedirect(reverse("student_feedback"))


# Rendering student profile page
def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request, "student_template/student_profile.html", {'user': user, 'student': student})


# Updating student profile
def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")

        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password != None and password != "":
                custom_user.set_password(password)
            custom_user.save()

            student = Students.objects.get(admin=custom_user)
            student.address = address
            student.save()
            messages.success(request, "Update profile successful")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to update profile")
            return HttpResponseRedirect(reverse("student_profile"))
