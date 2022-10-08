import json
from tabnanny import check
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Staffs, Subjects, SessionYearModel, Students, Attendance, AttendanceReport, LeaveReportStaff, FeedbackStaff, CustomUser, Courses, NotificationStaff,StudentResult
from django.contrib import messages
from django.urls import reverse


# Rendering staff_home page
def staff_home(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(
        course_id__in=final_course).count()

    # All attendance count
    attendance_count = Attendance.objects.filter(
        subject_id__in=subjects).count()

    # All leave count
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(
        staff_id=staff.id, leave_status=1).count()

    # Attendance data by subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(
            subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    students_list = []
    students_list_attendance_present = []
    students_list_attendance_absent = []

    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(
            status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(
            status=False, student_id=student.id).count()
        students_list.append(student.admin.username)
        students_list_attendance_present.append(attendance_present_count)
        students_list_attendance_absent.append(attendance_absent_count)

    return render(request, "staff_template/staff_home_template.html", {'students_count': students_count, 'attendance_count': attendance_count, 'leave_count': leave_count, 'subject_count': subjects, 'attendance_list': attendance_list, 'subject_list': subject_list, 'student_list': students_list, 'present_list': students_list_attendance_present, 'absent_list': students_list_attendance_absent})


# Fetching attendance
def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "staff_template/staff_take_attendance.html", {'subjects': subjects, 'session_years': session_years})


# Getting students
@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year)
    students = Students.objects.filter(
        course_id=subject.course_id, session_year_id=session_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id,
                      "name": student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Save attendance
@csrf_exempt
def save_attendance_data(request):
    student_id = request.POST.get("student_id")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")
    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year_id)
    json_student = json.loads(student_id)

    try:
        attendance = Attendance(subject_id=subject_model,
                                attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(
                student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


# Rendering staff_update_attendance page
def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.object.all()
    return render(request, "staff_template/staff_update_attendance.html", {'subjects': subjects, 'session_year_id': session_year_id})


# Getting attendance date
@csrf_exempt
def get_attendance_date(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []

    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


# Getting student attendance
@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Save updated student attendance
@csrf_exempt
def save_updateattendance_data(request):
    student_id = request.POST.get("student_id")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    json_student = json.loads(student_id)

    try:
        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(
                student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


# Rendering staff_leave page
def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_apply_leave.html", {'leave_data': leave_data})


# Saving staff leave
def staff_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(
                staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully applied for leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed to applied for leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


# Rendering staff_feedback page
def staff_feedback(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedbackStaff.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/staff_feedback.html", {'feedback_data': feedback_data})


# Saving staff feedback
def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            feedback = FeedbackStaff(
                staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Thankyou for feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Feedback submission failed")
            return HttpResponseRedirect(reverse("staff_feedback"))


# Rendering staff profile page
def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    return render(request, "staff_template/staff_profile.html", {'user': user, 'staff': staff})


# Updating staff profile
def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
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

            staff = Staffs.objects.get(admin=custom_user.id)
            staff.address = address
            staff.save()
            messages.success(request, "Update profile successful")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to update profile")
            return HttpResponseRedirect(reverse("staff_profile"))


# Saving FCM token
@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staffs.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# Rendering staff notification page
def staff_all_notification(request):
    staff = Staffs.objects.get(admin=request.user.id)
    notifications = NotificationStaff.objects.filter(staff_id=staff.id)
    return render(request, "staff_template/all_notification.html", {'notification': notifications})


# Rendering staff result page
def staff_add_result(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "staff_template/staff_add_result.html", {'subjects': subjects,'session_years':session_years})


# Saving student result
def save_student_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect('staff_add_result')
    else:
        student_admin_id = request.POST.get("student_list")
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')
        subject_obj  = Subjects.objects.get(id=subject_id)
        student_obj = Students.objects.get(admin=student_admin_id)
        try:
            check_exist = StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result updated successfully")
                return HttpResponseRedirect(reverse("staff_add_result"))
            else:
                result = StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result added successfully")
                return HttpResponseRedirect(reverse("staff_add_result"))
        except:
            messages.error(request, "Failed to add result")
            return HttpResponseRedirect(reverse("staff_add_result"))