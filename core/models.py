from django.db import models
import re
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.


class Customuser(models.Model):
    name=models.TextField(null=False)
    username=models.TextField(null=True, unique=True) #optionel
    email= models.EmailField(null=False, max_length=254)
    password=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.username
    def Email_valid(Email):
        pattern = r'^[a-zA-Z0-9]+([_.+%-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        match = re.search(pattern,Email)
        return bool(match)
    
    

#needs API to stock the data
class Session_model(models.Model):
    session_id = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)



class Workspace(models.Model):
    id_workspace=models.CharField(max_length=40,primary_key=True)
    name=models.TextField(max_length=30,null=False,blank=False)
    description=models.TextField(max_length=100,null=True,blank=True)
    owner=models.ForeignKey(Customuser, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    


class Workspacemembers(models.Model):    #many to many between Workspace and Customuser
    id_workspace=models.ForeignKey(Workspace,on_delete=models.CASCADE)
    member=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    isapproved=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
class notification(models.Model):
    member=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    notificationheader=models.TextField(max_length=20,null=False,blank=False)
    notificationbody=models.TextField(max_length=100,null=False,blank=False)
    isseen=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    id_task=models.CharField(max_length=40, primary_key=True)
    name=models.TextField(max_length=30,null=False,blank=False)
    
    sub_owner=models.ForeignKey(Customuser, on_delete=models.CASCADE)
    assossiatedto=models.ForeignKey(Workspace,on_delete=models.CASCADE)
   
    #reminder and notifications
    priority=models.IntegerField(null=False,blank=False,default=1)
    is_active=models.BooleanField(default=True)
    task_header=models.CharField(max_length=40)
    task_brifings=models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Set the end_at field to one day after the created_at date by default when the object is created
        if not self.end_at and not self.id_task:
            self.end_at = self.created_at + timezone.timedelta(days=1)
        super(Task, self).save(*args, **kwargs)

class Taskmembers(models.Model):   #many to many between task and Workspacemembers
    id_task=models.ForeignKey(Task,on_delete=models.CASCADE)
    member = models.ForeignKey(Workspacemembers, on_delete=models.CASCADE)
    isapproved=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)



class Contactsend(models.Model):
    subject=models.TextField(max_length=30,null=False,blank=False)
    content=models.TextField(max_length=300,null=False,blank=False)
    sentby=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)

