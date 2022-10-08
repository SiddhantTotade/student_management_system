from django.views import View
from django.shortcuts import render
from .forms import EditResultForm


class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        staff_id = request.user.id
        edit_result_form = EditResultForm(staff_id=staff_id)
        return render(request,"staff_template/edit_student_result.html",{'form':edit_result_form})
    
    def post(self,request,*args,**kwargs):
        pass