from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class CounsellorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class CounsellorForm(forms.ModelForm):
    class Meta:
        model=models.Counsellor
        fields=['address','mobile','department','status','profile_pic']



#for teacher related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class StudentForm(forms.ModelForm):
    #this is the extrafield for linking Student and their assigend Counsellor
    #this will show dropdown __str__ method Counsellor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Counsellor model and return it
    assignedCounsellorId=forms.ModelChoiceField(queryset=models.Counsellor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Student
        fields=['address','mobile','status','symptoms','profile_pic']



class AppointmentForm(forms.ModelForm):
    counsellorId=forms.ModelChoiceField(queryset=models.Counsellor.objects.all().filter(status=True),empty_label="Counsellor Name and Department", to_field_name="user_id")
    studentId=forms.ModelChoiceField(queryset=models.Student.objects.all().filter(status=True),empty_label="Student Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class StudentAppointmentForm(forms.ModelForm):
    counsellorId=forms.ModelChoiceField(queryset=models.Counsellor.objects.all().filter(status=True),empty_label="Counsellor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




