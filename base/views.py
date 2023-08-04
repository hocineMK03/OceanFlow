from django.shortcuts import render,redirect
from .forms import userformreg,userformlog
from core.models import Customuser,Session_model,Contactsend,Workspace,Task,Workspacemembers,notification,Taskmembers
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404
import base64
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime

# Create your views here.


def hashingcode(passw,name):
    if passw is not None:
        ascii_list = []
        for p in passw:
            ascii_val = str(ord(p))
            ascii_list.append(ascii_val)
        if name is not None:

            for n in name:
                ascii_val = str(ord(n))
                ascii_list.append(ascii_val)
        
        
        ascii_string = ''.join(ascii_list)
        print(ascii_string)
        return ascii_string
    return passw



def fornav(request,authent,workplaced):
    
    context={
          'authent':authent,
          'workplaced':workplaced,
     }
    return render(request,'navbar.html',context)

def home(request):
    session_id = request.COOKIES.get('session_id')
    authent = False

    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            print(sessioncust.user.Name)
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")

    fornav(request, authent, '1')
    context = {
        'authent': authent,
    }
    return render(request, 'base_templates/home.html', context)



def log(request):
    username = ""
    wrong = False
    session = None
    p=Customuser()
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        try:
            user = Customuser.objects.get(username=username)

            # Compare the hashed password from the input with the stored hashed password
            print(password)
            passw=hashingcode(password,username)
            
            if passw==user.password:
                session_id = str(uuid.uuid4())
                try:
                    session = Session_model.objects.get(session_id=session_id)
                except Session_model.DoesNotExist:
                    session = Session_model.objects.create(session_id=session_id, user=user)

                response = redirect('afterlog')
                response.set_cookie('session_id', session.session_id)
                return response
            else:
                messages.error(request, "Password not valid")
        except Customuser.DoesNotExist:
            wrong = True
            messages.error(request, "Username not valid")
            print("Does not exist")

    context = {
        'wrong': wrong,
    }
    return render(request, 'base_templates/login_page.html', context)



def reg(request):
        session=None
        password_list = []
        if request.method=='POST':
            username=request.POST.get('Username')  
            email=request.POST.get('Email')
            try:
                #check if the  username already exist
                user=Customuser.objects.get(username=username)
                
                print("here1")
                #user with email exist
            except Customuser.DoesNotExist:
                
                print("here2")
                if Customuser.Email_valid(email):
                    passw = request.POST.get('Password')
                    
                    ascii_string=hashingcode(passw,username)
                    
                    user=Customuser()
                    user.name=request.POST.get('Name')
                    user.username=username
                    user.email=email
                    
                    user.password=ascii_string

                    user.save()
                    while True:
                        session_id = str(uuid.uuid4())
                        print(session_id)
                        try:
                            # Try to retrieve a session with the generated session_id and user
                            session = Session_model.objects.get(session_id=session_id)
                            print(session)
                            
                        except Session_model.DoesNotExist:
                            # If a session with the same session_id does not exist, create a new session
                            session=Session_model.objects.create(session_id=session_id, user=user)
                           
                            response = redirect('afterlog')
                            response.set_cookie('session_id', session.session_id)
                            return response
                    
                    
                 
        context={}
        return render(request,'base_templates/register_page.html',context)



def logo(request):

    
    session_id=request.COOKIES.get('session_id')
    print(session_id)
    if session_id:
        session = Session_model.objects.get(session_id=session_id)
        response = redirect('home')
        response.delete_cookie('session_id')
        print("yes")
        # session.delete()
        return response

    context={
        
    }
    return render(request,'base_templates/home.html',context)


def aboutus(request):
    session_id = request.COOKIES.get('session_id')
    authent = False
   
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            print(sessioncust.user.name)
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in1")

    
    fornav(request, authent, False)
    context={
        'authent':authent,
    }
    return render(request,'base_templates/aboutus.html',context)


def contactus(request):
    session_id = request.COOKIES.get('session_id')
    authent = False
    u = None
    print("yes we're here")
    
    if session_id is not None:
        session = Session_model.objects.get(session_id=session_id)
        u=session.user
        u=Customuser.objects.get(id=u.id)
        authent=True
    else:
         authent=False
         return redirect('log')


    if request.method == 'POST':
        subject = request.POST.get('Subject')
        content = request.POST.get('Content')
        contact = Contactsend()
        contact.subject = subject
        contact.content = content
        if u:
            contact.sentby = u
        contact.save()
        return redirect('home')

    context = {
        'authent': authent,
    }
    return render(request, 'base_templates/contactus.html', context)








def afterlog(request):
    
    session_id=request.COOKIES.get('session_id')
    print(session_id)
    u=""
    print("hi")
    work=""
    work2=""
    if session_id is not None:
        session = Session_model.objects.get(session_id=session_id)
        u=session.user
        u=Customuser.objects.get(id=u.id)
        authent=True
    else:
         authent=False

    
   
    if(authent==False):
        response = redirect('home')
        
        return response

    fornav(request,authent,authent)
    if request.method=='POST':
            form_name=request.POST.get('form_name')
            if(form_name=='form1'):
                name=request.POST.get('name')
                if (name is None or name == ''):
                    print('--')
                    
                else:
                    workplace1=Workspace()
                    workplace1.name=name
                
                    idgenerated=hashingcode(name,u.name)
                    workplace1.id_workspace=idgenerated
                    workplace1.owner=u
                    workplace1.created_at = timezone.now()  
                    workplace1.save()
                    print("testest")
                    response = redirect('afterlog')
                    return response
            elif(form_name=="form2"):
                urltxt=request.POST.get('decoded_url').strip('\x00')
                print(urltxt,repr(urltxt))
               

                try:
                    workplaceid = Workspace.objects.get(id_workspace=str(urltxt))
                    if(workplaceid is not None):
                        try:
                            approving=Workspacemembers.objects.get(id_workspace=workplaceid,member=u.id)
                            if(approving.isapproved==True):
                                print("he can join")
                                original_string = urltxt

                                # Encode the string to base64
                                encoded_bytes = base64.b64encode(original_string.encode('utf-8'))

                                # Convert the bytes to a string (if you want a string representation)
                                encoded_string = encoded_bytes.decode('utf-8')
                                print(encoded_string)
                                response = redirect('workplace')
                                response.set_cookie('workspace_id',encoded_string)
                            
                                return response
                            else:
                                print('he is in the waiting list')
                        except:

                            if(u==workplaceid.owner):
                                print("he is already the owner")
                                encoded_bytes = base64.b64encode(original_string.encode('utf-8'))

                                # Convert the bytes to a string (if you want a string representation)
                                encoded_string = encoded_bytes.decode('utf-8')
                                print(encoded_string)
                                response = redirect('workplace')
                                response.set_cookie('workspace_id',encoded_string)
                                return response
                            
                            else:

                            
                                Workspacemembers1=Workspacemembers()
                                Workspacemembers1.id_workspace=workplaceid
                                Workspacemembers1.member=u
                                Workspacemembers1.isapproved=False
                                Workspacemembers1.save()
                                print("going for waitlist")
                                response = redirect('afterlog')
            
                                return response


                        
                except Workspace.DoesNotExist:
                    print("h")
                
    context={'authent':authent,
             'work':work,
             'work2':work2,
             }
        
    whichwork=request.COOKIES.get('whichwork')
    if(whichwork is not None):
        whichwork=int(whichwork)
        if(whichwork==1):
            work=Workspace.objects.filter(owner=u)
            context={'authent':authent,
             'work':work,
             'work2':work2,
             }
        elif(whichwork==2):
            work2=Workspacemembers.objects.filter(member=u.id,isapproved=True)
            context={'authent':authent,
             'work':work,
             'work2':work2,
             }
    else:
        work=Workspace.objects.filter(owner=u)
        context={'authent':authent,
             'work':work,
             'work2':work2,
             }
        
    
    
    return render(request,'base_templates/workplacehome.html',context)



def workplace(request):
    print("he is there he is there")
    session_id = request.COOKIES.get('session_id')
    
    authent = False
    workplaced=False
    u=""
    u1=""
    cansee=False
    sub_owner=""
    if session_id is not None:
        
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            u=sessioncust.user
            authent=True
            print(u.name)
        except:
            authent=False
        # try:
        #     workplaceexist=Workspace.objects.get(id_workspace=workspace_id)
        #     u1=workplaceexist
        #     print(u1.owner.name)
        #     workplaced=True
        # except:
        #     workplaced=False
        #     print("didn't")

        # if u.id==u1.owner.id:
        #     print("owner")
        #     #set rights
        # else:
        #     print("members")



#setting up the workplace




        workspace_id = request.COOKIES.get('workspace_id')
        print(workspace_id)
        decoded_bytes = base64.b64decode(workspace_id)

        # Convert the bytes to a string (text data)
        decoded_string = decoded_bytes.decode('utf-8')

        # Now, 'decoded_string' contains the decoded numeric ID as a text string
        # You can convert it back to an integer if needed
        decoded_id = int(decoded_string)

        # Example usage:
       
       
        workplaceid = Workspace.objects.get(id_workspace=str(decoded_id))
        print(workplaceid)
        if(workplaceid.owner==u):
            cansee=True
        if(request.method=='POST'):
            name=request.POST.get('name')
            sub_owner=request.POST.get('sub_owner')
            sub_owner=Customuser.objects.get(name=sub_owner)
           
            if(sub_owner is None):
                sub_owner=u
            task=Task()
            idgenerated=hashingcode(name,u.name)
            task.id_task=idgenerated
            task.name=name
            task.sub_owner=sub_owner
            task.assossiatedto=workplaceid
            
            task.save()
        tasks=Task.objects.filter(assossiatedto=workplaceid)
        

        allmembers=Workspacemembers.objects.filter(id_workspace=workplaceid,isapproved=True)
        subowners_list=[]
        members_list=[]
        
                

        try:
            allsubowners=Task.objects.filter(assossiatedto=workplaceid)

            for a in allsubowners:
                
                taskid=a.id_task
                
                try:
                    members=Taskmembers.objects.filter(id_task=taskid,isapproved=True)
                     
                    for mem in members:
                       
                        members_list.append(mem.member.member.name)
                        
                    print('w',members_list)  
                        
                    subowners_dict={
                            'name':a.name,
                            'subowner':a.sub_owner.name,
                            'members_list': members_list,
                        }
                    subowners_list.append(subowners_dict)
                    members_list=[] 
                except:
                    print("no tasks why")
        except:
            print("no tasks")
                    


       
    
    print("Subowners list:", subowners_list)
    # print("Members list:", members_list)
    
    fornav(request,authent,True)
    context={
        'authent':authent,
        'workplaced':workplaced,
        'cansee':cansee,
        'tasks':tasks,
        'allmembers':allmembers,
        'subowners_list':subowners_list,
        
    }
    return render(request,'base_templates/workplacemain.html',context)



def notifications(request):
    session_id = request.COOKIES.get('session_id')
    
    authent = False
    s=""
    u=""
    u1=""
    lista=[]
    
    if session_id is not None:
        
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            u=sessioncust.user
            authent=True
            print(u.name)
        except:
            authent=False

    
    if(authent==False):
        response = redirect('log')
        
        return response
    



    theobj=""
    tmp = request.COOKIES.get('whichnotif')
    if(tmp is None):
        print("why")
        theobj=notification.objects.filter(member=u.id)
        s="forth"

    else:

        tmp = int(tmp) 
        s=""
       
        if(tmp==1):
            theobj=notification.objects.filter(member=u.id)
            s="first"
            for n in theobj:
             print(n.notificationheader)
        elif(tmp==2):
            s="second"
        elif(tmp==3):
            print("tmp,",tmp)
            theobj=Workspacemembers.objects.filter(member=u.id,isapproved=False)
            
            s="third"
            
        else:
            his_workspaces=Workspace.objects.filter(owner=u.id)

            for his in his_workspaces:

                theobj=Workspacemembers.objects.filter(id_workspace=his,isapproved=False)
                lista.extend(theobj)

            
            
            
            s="forth"
            if(request.method=='POST'):
                tmp1 = request.COOKIES.get('whichbutton')
                tmp1=int(tmp1)
                hiddenid=request.POST.get('hiddenid')
                hiddenmember=request.POST.get('hiddenmember')
                print(hiddenid,"hidden",u)
                workplaceid=Workspacemembers.objects.filter(id_workspace=str(hiddenid),member=hiddenmember,isapproved=False).first()
                print(workplaceid,"hidden",u)
                
                if(workplaceid is not None):
                    hiddenmember=Customuser.objects.get(id=hiddenmember)
                    if(tmp1==1):
                        print("hi i am here")
                        workplaceid.isapproved=True
                        
                        notif=notification()
                        notif.member=hiddenmember
                        notif.notificationheader="you're accepted"
                        notif.notificationbody=str(u.name)+" has approved your invitation,congrats"
                        notif.save()
                        workplaceid.save()

                    elif(tmp1==2):
                        print("hi i am here")
                        notif=notification()
                        notif.member=hiddenmember
                        notif.notificationheader="you're not accepted"
                        notif.notificationbody=str(u.name)+" has declined your invit, i am sorry"
                        notif.save()
                        workplaceid.delete()
                        

        
    

    context={
        'theobj':theobj,
        'tmp':s,
        'lista':lista,
    }
    return render(request,'base_templates/notifications.html',context)


def task(request):
    session_id = request.COOKIES.get('session_id')
    
    authent = False
  
    u=""
    cansee=False
    
    if session_id is not None:
        
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            u=sessioncust.user
            authent=True
            print(u.name)
        except:
            authent=False

    
    if(authent==False):
        response = redirect('log')
        
        return response
    tmp1 = request.COOKIES.get('whichtask')
    if( tmp1 is not None):
            tmp1=int(tmp1)
            taskid=Task.objects.get(id_task=tmp1)
            print(taskid)
      

            if(request.method=='POST'):
                header=request.POST.get('header')
                content=request.POST.get('content')
                deadline=request.POST.get('deadline')
                startat=taskid.created_at
                taskid.task_header=header
                taskid.task_brifings=content
                taskid.end_at=deadline
                print(deadline)
                taskid.save()
            else:
                header=taskid.task_header
                content=taskid.task_brifings
                deadline=taskid.end_at
                startat=taskid.created_at
                print(deadline)
            task_leader=taskid.sub_owner
            workspace_leader=taskid.assossiatedto.owner
            if(task_leader==u or workspace_leader==u):
                cansee=True

    context={
        'authent':authent,
        'cansee':cansee,
        'header':header,
        'content':content,
        'deadline':deadline,
        'startat':startat,
    }
    return render(request,'base_templates/showtasks.html',context)













