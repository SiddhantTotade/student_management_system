from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Subjects, SessionYearModel, Students


# Rendering staff_home page
def staff_home(request):
    return render(request, "staff_template/staff_home_template.html")


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
    student_data = serializers.serialize("python", students)
    return JsonResponse(student_data, content_type="application/json", safe=False)
