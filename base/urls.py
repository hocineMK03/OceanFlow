from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name='home'),
    path('login',views.log,name='log'),
    path('register',views.reg,name='reg'),
    path('logout',views.logo,name='logout'),
    path('home/AboutUs',views.aboutus,name='aboutus'),
    path('home/ContactUs',views.contactus,name='contactus'),
    path('started',views.afterlog,name='afterlog'),
    path('workplace',views.workplace,name='workplace'),
    path('notifications',views.notifications,name='notifications'),
    path('task',views.task,name='task'),
]