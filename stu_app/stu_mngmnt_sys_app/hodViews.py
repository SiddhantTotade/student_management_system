from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from stu_mngmnt_sys_app.models import CustomUser, Courses, Subjects, Staffs, Students


# Redndering home page
def admin_home(request):
    return render(request, 'hod_template/home_content.html')


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
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed to add staff")
            return HttpResponseRedirect("/add_staff")


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
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed to add course")
            return HttpResponseRedirect("/add_course")


# Rendering add_student page
def add_student(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/add_student_template.html', {'courses': courses})


# Adding students
def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.session_start_year = session_start
            user.students.session_end_year = session_end
            user.students.gender = sex
            user.students.profile_pic = ""
            user.save()
            messages.success(request, "Student added successfully")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Failed to add student")
            return HttpResponseRedirect("/add_student")


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
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Failed to add subject")
            return HttpResponseRedirect("/add_subject")


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
    return render(request, "hod_template/edit_staff_template.html", {'staff': staff})


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
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except:
            messages.error(request, "Failed to edit staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)


# Rendering edit_student page
def edit_student(request, student_id):
    courses = Courses.objects.all()
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student_template.html", {'student': student, 'courses': courses})


# Editing student
def edit_student_save(request):
    pass
