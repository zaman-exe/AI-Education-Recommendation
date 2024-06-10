from django.contrib import admin
from .models import Counsellor,Student,Appointment,StudentDischargeDetails
# Register your models here.
class CounsellorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Counsellor, CounsellorAdmin)

class StudentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Student, StudentAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class StudentDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentDischargeDetails, StudentDischargeDetailsAdmin)
