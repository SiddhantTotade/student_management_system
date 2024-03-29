import json
from django.urls import reverse
from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from stu_mngmnt_sys_app.models import CustomUser, Courses, Subjects, NotificationStaff, NotificationStudent, SessionYearModel, Staffs, Students, FeedbackStaff, FeedbackStudent, LeaveReportStaff, LeaveReportStudent, Attendance, AttendanceReport
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


# Redndering home page
def admin_home(request):
    student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        student = Students.objects.filter(course_id=course.id).count()
        subject = Subjects.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subject)
        student_count_list_in_course.append(student)

    # Total student in each subject
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # Staff leave vs attendance
    staffs_all = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []
    for staff in staffs_all:
        subject_id = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_id).count()
        leave = LeaveReportStaff.objects.filter(
            staff_id=staff.id, leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leave)
        staff_name_list.append(staff.admin.username)

    # Student leave vs attendance
    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False).count()
        leave = LeaveReportStudent.objects.filter(
            student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leave+absent)
        student_name_list.append(student.admin.username)

    return render(request, 'hod_template/home_content.html', {'student_count': student_count, 'subject_count': subject_count, 'course_count': course_count, 'staff_count': staff_count, 'course_name_list': course_name_list, 'subject_count_list': subject_count_list, 'student_count_list_in_course': student_count_list_in_course, 'student_count_list_in_subject': student_count_list_in_subject, 'subject_list': subject_list, 'staff_name_list': staff_name_list, 'attendance_present_list_staff': attendance_present_list_staff, 'attendance_absent_list_staff': attendance_absent_list_staff, 'attendance_absent_list_student': attendance_absent_list_student, 'student_name_list': student_name_list, 'attendance_present_list_student': attendance_present_list_student})


# Rendering add_staff page
def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')


# Adding new staff and details.
def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff added successfully")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to add staff")
            return HttpResponseRedirect(reverse("add_staff"))


# Rendering add_course page
def add_course(request):
    return render(request, 'hod_template/add_course_template.html')


# Adding courses
def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Method not allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course added successfully")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to add course")
            return HttpResponseRedirect(reverse("add_course"))


# Rendering add_student page
def add_student(request):
    form = AddStudentForm()
    return render(request, 'hod_template/add_student_template.html', {'form': form})


# Adding students
def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(
                    username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year = SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender = sex
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student added successfully")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to add student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'hod_template/add_student_template.html', {'form': form})


# Rendering add_subject page
def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_template/add_subject_template.html', {'courses': courses, 'staffs': staffs})


# Adding subject
def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject added successfully")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to add subject")
            return HttpResponseRedirect(reverse("add_subject"))


# Rendering manage_staff page
def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/manage_staff_template.html', {'staffs': staffs})


# Rendering manage_student page
def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student_template.html', {'students': students})


# Rendering manage_course page
def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/manage_course_template.html', {'courses': courses})


# Rendering manage_subject page
def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'hod_template/manage_subject_template.html', {'subjects': subjects})


# Rendering edit_staff page
def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {'staff': staff, 'id': staff_id})


# Editing staff
def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Edit staff successful")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to edit staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


# Rendering edit_student page
def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id
    return render(request, "hod_template/edit_student_template.html", {'form': form, 'id': student_id, 'username': student.admin.username})


# Editing student
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        student_id = request.session.get("student_id")

        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                session_year = SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id = session_year
                student.gender = sex
                course = Courses.objects.get(id=course_id)
                student.course_id = course

                if profile_pic_url != None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request, "Edit student successful")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id': student_id}))
            except:
                messages.error(request, "Failed to edit student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id': student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, 'hod_template/edit_student_template.html', {'form': form, 'id': student_id, 'username': student.admin.username})


# Rendering edit_subject page
def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html", {'subject': subject, 'staffs': staffs, 'courses': courses, 'id': subject_id})


# Editing subject
def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        print(subject_name)
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            messages.success(request, "Edit course successful")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id': subject_id}))
        except:
            messages.error(request, "Failed to edit course")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id': subject_id}))


# Rendering edit_course page
def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {'course': course, 'id': course_id})


# Editing course
def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Edit course successful")
            return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id': course_id}))
        except:
            messages.error(request, "Failed to edit course")
            return HttpResponseRedirect(reverse("edit_course",  kwargs={'course_id': course_id}))


# Rendering manage_session page
def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


# Adding session
def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            session_year = SessionYearModel(
                session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()
            messages.success(request, "Added session successful")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to add session")
            return HttpResponseRedirect(reverse("manage_session"))


# Checking email exist or not
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# Checking username exist or not
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# Rendering student feedback page
def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, "hod_template/student_feedback_template.html", {'feedbacks': feedbacks})


# Repling message of student
@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# Rendering staff feedback page
def staff_feedback_message(request):
    feedbacks = FeedbackStaff.objects.all()
    return render(request, "hod_template/staff_feedback_template.html", {'feedbacks': feedbacks})


# Replying message of staff
@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# Rendering student leave view
def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request, "hod_template/student_leave_view.html", {'leaves': leaves})


# Rendering staff leave view
def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {'leaves': leaves})


# Approving leave for studeent
def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


# Disapproving leave for studeent
def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


# Approving leave for studeent
def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


# Disapproving leave for studeent
def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


# Rendering admin view attendance page
def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.object.all()
    return render(request, "hod_template/admin_view_attendance.html", {'subjects': subjects, 'session_year_id': session_year_id})


# Rendering admin view attendance page
@csrf_exempt
def admin_get_attendance_date(request):
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


# Rendering admin view attendance student
@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Rendering admin profile page
def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {'user': user})


# Updating admin profile
def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password != None and password != "":
                custom_user.set_password(password)
            custom_user.save()
            messages.success(request, "Update profile successful")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to update profile")
            return HttpResponseRedirect(reverse("admin_profile"))


# Rendering staff notification page
def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/staff_notification.html", {'staffs': staffs})


# Rendering student notification page
def admin_send_notification_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/student_notification.html", {'students': students})


# Sending notification to student
@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student = Students.objects.get(admin=id)
    token = student.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://stu-mngmnt-sys.herokuapp.com/student_all_notification",
            "icon": "https://stu-mngmnt-sys.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=AAAAWkNzMZE:APA91bH8aQURWQ1kBUx9-sJXa8tbl1UjYyuixweprTaudT7reKwOG0PWAhMiz8JgYzcQfPatbOaNlqcC_DSrUca0o8xkl9kUUfsH08AI5ysylXY4sCavwDbUjbSzEylCXrLOOxQkRfyh"}
    data = request.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStudent(student_id=student, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


# Sending notification to staff
@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(admin=id)
    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://stu-mngmnt-sys.herokuapp.com/staff_all_notification",
            "icon": "https://stu-mngmnt-sys.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=AAAAWkNzMZE:APA91bH8aQURWQ1kBUx9-sJXa8tbl1UjYyuixweprTaudT7reKwOG0PWAhMiz8JgYzcQfPatbOaNlqcC_DSrUca0o8xkl9kUUfsH08AI5ysylXY4sCavwDbUjbSzEylCXrLOOxQkRfyh"}
    data = request.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaff(staff_id=staff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")
