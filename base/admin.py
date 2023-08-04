from django.contrib import admin
from core.models import Customuser,Session_model,Workspace,Workspacemembers,notification,Task,Taskmembers
# Register your models here.


admin.site.register(Customuser)
admin.site.register(Session_model)
admin.site.register(Workspace)
admin.site.register(Workspacemembers)
admin.site.register(notification)
admin.site.register(Task)
admin.site.register(Taskmembers)