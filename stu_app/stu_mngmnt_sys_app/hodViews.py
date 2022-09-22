from django.shortcuts import render


# Redndering home page
def admin_home(request):
    return render(request, 'hod_template/home_content.html')


# Rendering add_staff page
def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')
