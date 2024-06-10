import json
import os
from django.shortcuts import render,redirect,reverse
from dotenv import load_dotenv
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime, time,timedelta,date
from django.conf import settings
from django.db.models import Q

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'education/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'education/adminclick.html')


#for showing signup/login button for Counsellor
def counsellorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'education/counsellorclick.html')


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'education/studentclick.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'education/adminsignup.html',{'form':form})




def counsellor_signup_view(request):
    userForm=forms.CounsellorUserForm()
    counsellorForm=forms.CounsellorForm()
    mydict={'userForm':userForm,'counsellorForm':counsellorForm}
    if request.method=='POST':
        userForm=forms.CounsellorUserForm(request.POST)
        counsellorForm=forms.CounsellorForm(request.POST,request.FILES)
        if userForm.is_valid() and counsellorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            counsellor=counsellorForm.save(commit=False)
            counsellor.user=user
            counsellor=counsellor.save()
            my_counsellor_group = Group.objects.get_or_create(name='Counsellor')
            my_counsellor_group[0].user_set.add(user)
        return HttpResponseRedirect('counsellorlogin')
    return render(request,'education/counsellorsignup.html',context=mydict)


def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.assignedCounsellorId=request.POST.get('assignedCounsellorId')
            student=student.save()
            my_student_group = Group.objects.get_or_create(name='Student')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'education/studentsignup.html',context=mydict)






#-----------for checking user is Counsellor , student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_counsellor(user):
    return user.groups.filter(name='Counsellor').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,Counsellor OR Student
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_counsellor(request.user):
        accountapproval=models.Counsellor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('counsellor-dashboard')
        else:
            return render(request,'education/counsellor_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'education/student_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    counsellors=models.Counsellor.objects.all().order_by('-id')
    students=models.Student.objects.all().order_by('-id')
    #for three cards
    counsellorcount=models.Counsellor.objects.all().filter(status=True).count()
    pendingcounsellorcount=models.Counsellor.objects.all().filter(status=False).count()

    studentcount=models.Student.objects.all().filter(status=True).count()
    pendingstudentcount=models.Student.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'counsellors':counsellors,
    'students':students,
    'counsellorcount':counsellorcount,
    'pendingcounsellorcount':pendingcounsellorcount,
    'studentcount':studentcount,
    'pendingstudentcount':pendingstudentcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'education/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_counsellor_view(request):
    return render(request,'education/admin_counsellor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_counsellor_view(request):
    counsellors=models.Counsellor.objects.all().filter(status=True)
    return render(request,'education/admin_view_counsellor.html',{'counsellors':counsellors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_counsellor_from_education_view(request,pk):
    counsellor=models.Counsellor.objects.get(id=pk)
    user=models.User.objects.get(id=counsellor.user_id)
    user.delete()
    counsellor.delete()
    return redirect('admin-view-counsellor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_counsellor_view(request,pk):
    counsellor=models.Counsellor.objects.get(id=pk)
    user=models.User.objects.get(id=counsellor.user_id)

    userForm=forms.CounsellorUserForm(instance=user)
    counsellorForm=forms.CounsellorForm(request.FILES,instance=counsellor)
    mydict={'userForm':userForm,'counsellorForm':counsellorForm}
    if request.method=='POST':
        userForm=forms.CounsellorUserForm(request.POST,instance=user)
        counsellorForm=forms.CounsellorForm(request.POST,request.FILES,instance=counsellor)
        if userForm.is_valid() and counsellorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            counsellor=counsellorForm.save(commit=False)
            counsellor.status=True
            counsellor.save()
            return redirect('admin-view-counsellor')
    return render(request,'education/admin_update_counsellor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_counsellor_view(request):
    userForm=forms.CounsellorUserForm()
    counsellorForm=forms.CounsellorForm()
    mydict={'userForm':userForm,'counsellorForm':counsellorForm}
    if request.method=='POST':
        userForm=forms.CounsellorUserForm(request.POST)
        counsellorForm=forms.CounsellorForm(request.POST, request.FILES)
        if userForm.is_valid() and counsellorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            counsellor=counsellorForm.save(commit=False)
            counsellor.user=user
            counsellor.status=True
            counsellor.save()

            my_counsellor_group = Group.objects.get_or_create(name='Counsellor')
            my_counsellor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-counsellor')
    return render(request,'education/admin_add_counsellor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_counsellor_view(request):
    #those whose approval are needed
    counsellors=models.Counsellor.objects.all().filter(status=False)
    return render(request,'education/admin_approve_counsellor.html',{'counsellors':counsellors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_counsellor_view(request,pk):
    counsellor=models.Counsellor.objects.get(id=pk)
    counsellor.status=True
    counsellor.save()
    return redirect(reverse('admin-approve-counsellor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_counsellor_view(request,pk):
    counsellor=models.Counsellor.objects.get(id=pk)
    user=models.User.objects.get(id=counsellor.user_id)
    user.delete()
    counsellor.delete()
    return redirect('admin-approve-counsellor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_counsellor_specialisation_view(request):
    counsellors=models.Counsellor.objects.all().filter(status=True)
    return render(request,'education/admin_view_counsellor_specialisation.html',{'counsellors':counsellors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'education/admin_student.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'education/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_education_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)

    userForm=forms.StudentUserForm(instance=user)
    studentForm=forms.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.status=True
            student.assignedCounsellorId=request.POST.get('assignedCounsellorId')
            student.save()
            return redirect('admin-view-student')
    return render(request,'education/admin_update_student.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            student=studentForm.save(commit=False)
            student.user=user
            student.status=True
            student.assignedCounsellorId=request.POST.get('assignedCounsellorId')
            student.save()

            my_student_group = Group.objects.get_or_create(name='Student')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-student')
    return render(request,'education/admin_add_student.html',context=mydict)



#------------------FOR APPROVING student BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    #those whose approval are needed
    students=models.Student.objects.all().filter(status=False)
    return render(request,'education/admin_approve_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    student.status=True
    student.save()
    return redirect(reverse('admin-approve-student'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')



#--------------------- FOR DISCHARGING Student BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_student_view(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'education/admin_discharge_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    days=(date.today()-student.admitDate) #2 days, 0:00:00
    assignedCounsellor=models.User.objects.all().filter(id=student.assignedCounsellorId)
    d=days.days # only how many day that is 2
    studentDict={
        'studentId':pk,
        'name':student.get_name,
        'mobile':student.mobile,
        'address':student.address,
        'symptoms':student.symptoms,
        'admitDate':student.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedCounsellorName':assignedCounsellor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'counsellorFee':request.POST['counsellorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['counsellorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        studentDict.update(feeDict)
        #for updating to database studentDischargeDetails (pDD)
        pDD=models.StudentDischargeDetails()
        pDD.studentId=pk
        pDD.studentName=student.get_name
        pDD.assignedCounsellorName=assignedCounsellor[0].first_name
        pDD.address=student.address
        pDD.mobile=student.mobile
        pDD.symptoms=student.symptoms
        pDD.admitDate=student.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.counsellorFee=int(request.POST['counsellorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['counsellorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'education/student_final_bill.html',context=studentDict)
    return render(request,'education/student_generate_bill.html',context=studentDict)



#--------------for discharge student bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.StudentDischargeDetails.objects.all().filter(studentId=pk).order_by('-id')[:1]
    dict={
        'studentName':dischargeDetails[0].studentName,
        'assignedCounsellorName':dischargeDetails[0].assignedCounsellorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'counsellorFee':dischargeDetails[0].counsellorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('education/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'education/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'education/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.counsellorId=request.POST.get('counsellorId')
            appointment.studentId=request.POST.get('studentId')
            appointment.counsellorName=models.User.objects.get(id=request.POST.get('counsellorId')).first_name
            appointment.studentName=models.User.objects.get(id=request.POST.get('studentId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'education/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'education/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ Counsellor RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_dashboard_view(request):
    #for three cards
    studentcount=models.Student.objects.all().filter(status=True,assignedCounsellorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,counsellorId=request.user.id).count()
    studentdischarged=models.StudentDischargeDetails.objects.all().distinct().filter(assignedCounsellorName=request.user.first_name).count()

    #for  table in Counsellor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,counsellorId=request.user.id).order_by('-id')
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid).order_by('-id')
    appointments=zip(appointments,students)
    mydict={
    'studentcount':studentcount,
    'appointmentcount':appointmentcount,
    'studentdischarged':studentdischarged,
    'appointments':appointments,
    'counsellor':models.Counsellor.objects.get(user_id=request.user.id), #for profile picture of counsellor in sidebar
    }
    return render(request,'education/counsellor_dashboard.html',context=mydict)



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_student_view(request):
    mydict={
    'counsellor':models.Counsellor.objects.get(user_id=request.user.id), #for profile picture of counsellor in sidebar
    }
    return render(request,'education/counsellor_student.html',context=mydict)





@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_view_student_view(request):
    students=models.Student.objects.all().filter(status=True,assignedCounsellorId=request.user.id)
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of counsellor in sidebar
    return render(request,'education/counsellor_view_student.html',{'students':students,'counsellor':counsellor})


@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def search_view(request):
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of counsellor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    students=models.Student.objects.all().filter(status=True,assignedCounsellorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'education/counsellor_view_student.html',{'students':students,'counsellor':counsellor})



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_view_discharge_student_view(request):
    dischargedstudents=models.StudentDischargeDetails.objects.all().distinct().filter(assignedCounsellorName=request.user.first_name)
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of Counsellor in sidebar
    return render(request,'education/counsellor_view_discharge_student.html',{'dischargedstudents':dischargedstudents,'counsellor':counsellor})



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_appointment_view(request):
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of Counsellor in sidebar
    return render(request,'education/counsellor_appointment.html',{'counsellor':counsellor})



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_view_appointment_view(request):
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of counsellor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,counsellorId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'education/counsellor_view_appointment.html',{'appointments':appointments,'counsellor':counsellor})



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def counsellor_delete_appointment_view(request):
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of counsellor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,counsellorId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'education/counsellor_delete_appointment.html',{'appointments':appointments,'counsellor':counsellor})



@login_required(login_url='counsellorlogin')
@user_passes_test(is_counsellor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    counsellor=models.Counsellor.objects.get(user_id=request.user.id) #for profile picture of counsellor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,counsellorId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'education/counsellor_delete_appointment.html',{'appointments':appointments,'counsellor':counsellor})



#---------------------------------------------------------------------------------
#------------------------ counsellor RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ Student RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    student=models.Student.objects.get(user_id=request.user.id)
    counsellor=models.Counsellor.objects.get(user_id=student.assignedCounsellorId)
    mydict={
    'student':student,
    'counsellorName':counsellor.get_name,
    'counsellorMobile':counsellor.mobile,
    'counsellorAddress':counsellor.address,
    'symptoms':student.symptoms,
    'counsellorDepartment':counsellor.department,
    'admitDate':student.admitDate,
    }
    return render(request,'education/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_appointment_view(request):
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of Student in sidebar
    return render(request,'education/student_appointment.html',{'student':student})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_book_appointment_view(request):
    appointmentForm=forms.StudentAppointmentForm()
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of Student in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'student':student,'message':message}
    if request.method=='POST':
        appointmentForm=forms.StudentAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('counsellorId'))
            desc=request.POST.get('description')

            counsellor=models.Counsellor.objects.get(user_id=request.POST.get('counsellorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.counsellorId=request.POST.get('counsellorId')
            appointment.studentId=request.user.id #----user can choose any student but only their info will be stored
            appointment.counsellorName=models.User.objects.get(id=request.POST.get('counsellorId')).first_name
            appointment.studentName=request.user.first_name #----user can choose any student but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('student-view-appointment')
    return render(request,'education/student_book_appointment.html',context=mydict)



def student_view_counsellor_view(request):
    counsellors=models.Counsellor.objects.all().filter(status=True)
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    return render(request,'education/student_view_counsellor.html',{'student':student,'counsellors':counsellors})



def search_counsellor_view(request):
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    counsellors=models.Counsellor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'education/student_view_counsellor.html',{'student':student,'counsellors':counsellors})




@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_appointment_view(request):
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of Student in sidebar
    appointments=models.Appointment.objects.all().filter(studentId=request.user.id)
    return render(request,'education/student_view_appointment.html',{'appointments':appointments,'student':student})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_discharge_view(request):
    student=models.Student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    dischargeDetails=models.StudentDischargeDetails.objects.all().filter(studentId=student.id).order_by('-id')[:1]
    studentDict=None
    if dischargeDetails:
        studentDict ={
        'is_discharged':True,
        'student':student,
        'studentId':student.id,
        'studentName':student.get_name,
        'assignedCounsellorName':dischargeDetails[0].assignedCounsellorName,
        'address':student.address,
        'mobile':student.mobile,
        'symptoms':student.symptoms,
        'admitDate':student.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'counsellorFee':dischargeDetails[0].counsellorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(studentDict)
    else:
        studentDict={
            'is_discharged':False,
            'student':student,
            'studentId':request.user.id,
        }
    return render(request,'education/student_discharge.html',context=studentDict)


#------------------------ student RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'education/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'education/contactussuccess.html')
    return render(request, 'education/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ API RELATED VIEWS Start ------------------------------
#---------------------------------------------------------------------------------


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai

@csrf_exempt
def recommend_careers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        questions = data['questions']  # List of questions
        answers = data['answers']  # List of user-selected answers
        options = data['options']  # List of options for each question
        careers = predict_careers(questions, answers, options)
        return JsonResponse({'careers': careers})
    else:
        return JsonResponse({'error': 'This endpoint only supports POST requests'}, status=405)

def predict_careers(questions, answers, options):
    prompt = generate_prompt(questions, answers, options)
    chatgpt_response = call_chatgpt_api(prompt)
    return chatgpt_response.split("\n")  # Assuming the response is a simple list of careers

def generate_prompt(questions, answers, options):
    prompt = "Based on the user's responses below, recommend five suitable career paths:\n\n"
    for question, answer, opts in zip(questions, answers, options):
        options_text = ', '.join(opts)
        prompt += f"Question: {question}\nOptions: {options_text}\nSelected: {answer}\n\n"
    return prompt

def call_chatgpt_api(prompt):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        print(api_key)
        client = openai.Client(api_key=api_key)
        max_attempts = 5
        base_sleep_seconds = 2  # Base sleep time which will increase exponentially

        for attempt in range(max_attempts):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    model="gpt-3.5-turbo-0125",
                    #response_format={"type": "json_object"},
                )
                return response.choices[0].message.content
            except openai.RateLimitError as e:
                sleep_time = base_sleep_seconds * (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {sleep_time} seconds.\n", e)
                time.sleep(sleep_time)
            except openai.OpenAIError as e:
                print(f"An OpenAI API error occurred: {e}")
                break
        print("Failed to get response after multiple retries.")
        return None
    
def test_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'education/test.html')


#---------------------------------------------------------------------------------
#------------------------ API RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
