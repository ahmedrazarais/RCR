from django.contrib import admin
from .models import Class,FileUpload,Announcement,Assignment,StudentSubmission,Message
# Register your models here.
admin.site.register(Class)
admin.site.register(FileUpload)

admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(StudentSubmission)
admin.site.register(Message)
