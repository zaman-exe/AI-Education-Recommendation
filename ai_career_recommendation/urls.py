




from django.contrib import admin
from django.urls import path
from education import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('counsellorclick', views.counsellorclick_view),
    path('studentclick', views.studentclick_view),

    path('adminsignup', views.admin_signup_view),
    path('counsellorsignup', views.counsellor_signup_view,name='counsellorsignup'),
    path('studentsignup', views.student_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='education/adminlogin.html')),
    path('counsellorlogin', LoginView.as_view(template_name='education/counsellorlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='education/studentlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='education/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-counsellor', views.admin_counsellor_view,name='admin-counsellor'),
    path('admin-view-counsellor', views.admin_view_counsellor_view,name='admin-view-counsellor'),
    path('delete-counsellor-from-education/<int:pk>', views.delete_counsellor_from_education_view,name='delete-counsellor-from-education'),
    path('update-counsellor/<int:pk>', views.update_counsellor_view,name='update-counsellor'),
    path('admin-add-counsellor', views.admin_add_counsellor_view,name='admin-add-counsellor'),
    path('admin-approve-counsellor', views.admin_approve_counsellor_view,name='admin-approve-counsellor'),
    path('approve-counsellor/<int:pk>', views.approve_counsellor_view,name='approve-counsellor'),
    path('reject-counsellor/<int:pk>', views.reject_counsellor_view,name='reject-counsellor'),
    path('admin-view-counsellor-specialisation',views.admin_view_counsellor_specialisation_view,name='admin-view-counsellor-specialisation'),


    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-education/<int:pk>', views.delete_student_from_education_view,name='delete-student-from-education'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-approve-student', views.admin_approve_student_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('reject-student/<int:pk>', views.reject_student_view,name='reject-student'),
    path('admin-discharge-student', views.admin_discharge_student_view,name='admin-discharge-student'),
    path('discharge-student/<int:pk>', views.discharge_student_view,name='discharge-student'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR counsellor RELATED URLS-------------------------------------
urlpatterns +=[
    path('counsellor-dashboard', views.counsellor_dashboard_view,name='counsellor-dashboard'),
    path('search', views.search_view,name='search'),

    path('counsellor-student', views.counsellor_student_view,name='counsellor-student'),
    path('counsellor-view-student', views.counsellor_view_student_view,name='counsellor-view-student'),
    path('counsellor-view-discharge-student',views.counsellor_view_discharge_student_view,name='counsellor-view-discharge-student'),

    path('counsellor-appointment', views.counsellor_appointment_view,name='counsellor-appointment'),
    path('counsellor-view-appointment', views.counsellor_view_appointment_view,name='counsellor-view-appointment'),
    path('counsellor-delete-appointment',views.counsellor_delete_appointment_view,name='counsellor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




#---------FOR student RELATED URLS-------------------------------------
urlpatterns +=[

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-appointment', views.student_appointment_view,name='student-appointment'),
    path('student-book-appointment', views.student_book_appointment_view,name='student-book-appointment'),
    path('student-view-appointment', views.student_view_appointment_view,name='student-view-appointment'),
    path('student-view-counsellor', views.student_view_counsellor_view,name='student-view-counsellor'),
    path('searchcounsellor', views.search_counsellor_view,name='searchcounsellor'),
    path('student-discharge', views.student_discharge_view,name='student-discharge'),

]

urlpatterns +=[

    path('test', views.recommend_careers, name='test-api'),

]
