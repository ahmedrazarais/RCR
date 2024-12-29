from django.urls import path
from . import views

urlpatterns = [
 

    path("" , views.teacher_home , name="teacher_home"),
    path("create_class/" , views.create_class , name="class_creation"),
    path("view_class/" , views.view_classes , name = "all_classess"),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'), 
    path('create_announcement/', views.make_announcement , name='announcement'),
    path('upload_assignment/', views.upload_assignment, name='upload_assignment'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('messages/', views.teacher_messages, name='teacher_messages'),
    


   


    

    
]

