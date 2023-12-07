from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from .models import *
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from django.core.mail import send_mail 
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from datetime import datetime



# Create your views here.


def login_user(request):
    
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
         
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('/pipelines')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('/')
        
    if request.method=="GET":
        return render(request, 'pages/login.html',{})
    
    
    return render(request, 'pages/login.html',{})

def logout_user(request):
    
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('/')


def validate_password(password):
    if len(password)<8:
        return False
    elif any(char.isalpha() for char in password)==False:
        return False
    elif any(char.isdigit() for char in password)==False:
        return False


def base(request):
    return render(request, 'base.html',{})

def add_pipeline(request):
    contacts_all=Contact.objects.all().filter(user_id=request.user.id).order_by(Lower('first_name'))
    contact_names=list(contacts_all.values('first_name','last_name','id'))
    if request.method=="GET":
        return render(request, 'pages/add-pipeline.html',{"contact_names":contact_names})

    
    if request.method=='POST':
        contact=request.POST.get('contact')
        stage=request.POST.get('stage')
        notes=request.POST.get('notes')
        user_id=request.user.id
        new_pipeline=Pipeline.objects.create(contact_id=contact, stage=stage, notes=notes, user_id=user_id)   
        
        try:
            new_pipeline.save()
            pipelines=Pipeline.objects.select_related('contact').filter(user_id=request.user.id)
            messages.success(request, "Successfully added!")
            return render(request, 'pages/get-pipelines.html',{"pipelines":pipelines, "stage_names":stage_names})
        except:
            messages.error(request, "An error occured!")
            alert_message="Please fill all the required fields"
            return render(request, 'pages/add-pipeline.html',{"contact_names":contact_names, "alert_message":alert_message})
   

stage_names={
    "1":"New Lead",
    "2":"Qualified",
    "3":"Meeting Scheduled",
    "4":"Proposal Made",
    "5":"Negotiating",
    "6":"Closed Won",
    "7":"Closed Lost"
}

def get_pipelines(request):
    if request.method=="GET":
        pipelines_all=Pipeline.objects.select_related('contact').filter(user_id=request.user.id)
        pipelines=pipelines_all
        return render(request, 'pages/get-pipelines.html',{'pipelines':pipelines, 'stage_names':stage_names})
        


def get_pipeline_detail(request, id):
    pipeline=get_object_or_404(Pipeline.objects.select_related('contact').filter(user_id=request.user.id), pk=id)

    if request.method=='GET':
        return render(request,"pages/pipeline-detail.html",{"pipeline":pipeline, "stage_names":stage_names})
    

def get_contacts(request, ):
    if request.method=="GET":
        contacts=Contact.objects.all().filter(user_id=request.user.id).order_by(Lower('first_name'))    
        contacts={"contacts":contacts}
        return render(request, 'pages/get-contacts.html',contacts)
        



def add_contact(request):
    if request.method=="GET":
        return render(request, 'pages/add-contact.html')
    
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        organization = request.POST.get('organization')
        organization = bool(organization) if organization =="on" else False
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        notes = request.POST.get('notes')
        user_id=request.user.id
        new_contact=Contact.objects.create(first_name=first_name, last_name=last_name, email=email, organization=organization, phone=phone, address=address, city=city, country=country, user_id=user_id)
 
        try:
            new_contact.save()
            messages.success(request, "Successfully added!")
            return render(request, 'pages/add-contact.html')
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/add-contact.html')


def get_contact_detail(request, id):
    contact=get_object_or_404(Contact.objects.filter(user_id=request.user.id), pk=id)

    if request.method=='GET':
        return render(request,"pages/contact-detail.html",{"contact":contact})
    
     
    
def edit_contact(request, id):
    try:
        contact=get_object_or_404(Contact.objects.filter(user_id=request.user.id), pk=id)
    except Http404:
        return render(request, 'pages/404.html') 
    
    if request.method=='GET':
        return render(request, 'pages/edit-contact.html', {"contact":contact})
    
    elif request.method=='POST':
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.email = request.POST.get('email')
        organization = request.POST.get('organization')
        contact.organization = bool(organization) if organization =="on" else False
        contact.phone = request.POST.get('phone')
        contact.address = request.POST.get('address')
        contact.city = request.POST.get('city')
        contact.country = request.POST.get('country')
        contact.notes = request.POST.get('notes')
        contact.user_id=request.user.id
        try:
            contact.save()
            messages.success(request, "Updated!")
            return render(request, 'pages/contact-detail.html',{"contact":contact})
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/edit-contact.html',{"contact":contact})
        

def delete_contact(request, id):
    try:
        contact=get_object_or_404(Contact.objects.filter(user_id=request.user.id), pk=id)
    except Http404:
        return render(request, 'pages/404.html')
    if request.method=='POST':
        contact.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('/contacts')

        
        

def edit_pipeline(request, id):
    try:
        pipeline=get_object_or_404(Pipeline.objects.select_related('contact').filter(user_id=request.user.id), pk=id)
        contacts_all=Contact.objects.all().filter(user_id=request.user.id).order_by(Lower('first_name'))
    except Http404:
        return render(request, "pages/404.html")
        
    if request.method=='GET':
        return render(request, 'pages/edit-pipeline.html', {"pipeline":pipeline, "contact_names":contacts_all, "stage_names":stage_names})
    
    elif request.method=='POST':
        pipeline.contact_id=request.POST.get('contact')
        pipeline.stage=request.POST.get('stage')
        pipeline.notes=request.POST.get('notes')
        pipeline.user_id=request.user.id
        try:
            pipeline.save()
            messages.success(request, "Updated!")
            return redirect('/pipelines')
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/edit-pipeline.html',{"pipeline":pipeline,"contact_names":contacts_all, "stage_names":stage_names})
                
       

def delete_pipeline(request, id):
    try:
        pipeline=get_object_or_404(Pipeline.objects.filter(user_id=request.user.id), pk=id)
    except Http404:
        return render(request, "pages/404.html")
    if request.method=='POST':
        pipeline.delete()
        messages.success(request, "You have successfully deleted!")
        return redirect('/pipelines')

def contact(request):
    if request.method=="POST":
        name_surname=request.POST["name_surname"]
        email=request.POST["email"]
        message=request.POST["message"]
        subject=request.POST["subject"]
        
        form_message=f"Contact form filled by: {name_surname} on {datetime.now().date()}\nEmail: {email}\n Subject : {subject}\n Message:\n{message}"
        send_mail(
            subject,
            form_message,
            email,
            ["pelinsualtun@gmail.com"],
            fail_silently=False,    
        )
        
        conf_message=render_to_string('pages/mail-template.html',{"name_surname":name_surname})
        send_mail(
            'Contact form confirmation',
            "",
            "pelinsualtun@gmail.com",
            [email],
            fail_silently=False,
            html_message=conf_message,
        )
        
        return HttpResponse("Thank you for your message!")
    return render(request, 'pages/mailform.html')


def register_user(request):
    if request.method=="GET":
        return render(request, 'pages/register.html')
    if request.method=="POST":
        username=request.POST["username"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        form={"username":username, "first_name":first_name, "last_name":last_name, "email":email, "password":password, "password2":password2}
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request,'pages/register.html',{"form":form})
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request,'pages/register.html',{"form":form})   
         
        elif validate_password(password)==False:
            messages.error(request, "Password must be at least 8 characters long and must contain at least one letter and one number!")
            return render(request,'pages/register.html',{"form":form})
        
        elif password!=password2:
            messages.error(request, "Passwords do not match!")
            return render(request,'pages/register.html',{"form":form})             
        else:
            user=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            messages.success(request, "You have successfully registered!")
            return redirect('/')


def get_events(request):
    date=datetime.now().date()
    if request.method=="GET":
        events=Event.objects.select_related('contact').filter(user_id=request.user.id,event_date__gte=date).order_by('event_date')
        return render(request, 'pages/get-events.html',{"events":events})


def add_event(request):
    contacts=Contact.objects.all().filter(user_id=request.user.id).order_by(Lower('first_name'))
    if request.method=="GET":
        return render(request, 'pages/add-event.html',{'contact_names':contacts})
        
    if request.method=='POST':
        contact=request.POST.get('contact')
        event_name=request.POST.get('event_name')
        event_date=request.POST.get('event_date')
        event_time=request.POST.get('event_time')
        event_location=request.POST.get('event_location')
        event_description=request.POST.get('event_description')
        user_id=request.user.id
        new_event=Event.objects.create(contact_id=contact, event_name=event_name, event_date=event_date, event_time=event_time, event_location=event_location, event_description=event_description, user_id=user_id)   
        
        try:
            new_event.save()
            messages.success(request, "Successfully added!")
            return redirect('/events')
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/add-event.html',{'contact_names':contacts})

        

def edit_event(request, id):
    try:
        event=get_object_or_404(Event.objects.select_related('contact').filter(user_id=request.user.id), pk=id)
        contacts_all=Contact.objects.all().filter(user_id=request.user.id).order_by(Lower('first_name'))
    except Http404:
        return render(request, "pages/404.html")
    
    if request.method=="GET":
        return render(request, 'pages/edit-event.html',{"event":event,'contact_names':contacts_all})
    
    elif request.method=="POST":
        event.contact_id=request.POST.get('contact')
        event.event_name=request.POST.get('event_name')
        event.event_date=request.POST.get('event_date')
        event.event_time=request.POST.get('event_time')
        event.event_location=request.POST.get('event_location')
        event.event_description=request.POST.get('event_description')
        event.user_id=request.user.id
        try:
            event.save()
            messages.success(request, "Updated!")
            return redirect('/events')
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/edit-event.html',{"event":event,'contact_names':contacts_all})
    



def delete_event(request,id):
    try:
        event=get_object_or_404(Event.objects.filter(user_id=request.user.id), pk=id)
    except Http404:
        return render(request, "pages/404.html")
    if request.method=="POST":
        try:
            event.delete()
            messages.success(request, "Successfully deleted!")
            return redirect('/events')
        except:
            messages.error(request, "An error occured!")
            return redirect('/events')
        
def get_event_detail(request,id):
    try:
        event=get_object_or_404(Event.objects.select_related('contact').filter(user_id=request.user.id), pk=id)
    except Http404:
        return render(request, "pages/404.html")
    if request.method=="GET":
        return render(request, 'pages/event-detail.html',{"event":event})
    
def edit_account(request):
    try:
        user=get_object_or_404(User.objects.all(), pk=request.user.id)
    except Http404:
        return render(request, "pages/404.html")
    if request.method=="GET":
        return render(request, 'pages/account.html',{"user":user})
    elif request.method=="POST":
        user.username=request.POST.get('username')
        if User.objects.filter(username=user.username).exclude(id=request.user.id).exists():
            alert_message="Username already exists!"    
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        if User.objects.filter(email=user.email).exclude(id=request.user.id).exists():
            alert_message="Email already exists!"
            return render(request, 'pages/account.html',{"user":user, "alert_message":alert_message})
        try:
            user.save()
            messages.success(request, "Updated!")
            return render(request, 'pages/account.html',{"user":user})
        except:
            messages.error(request, "An error occured!")
            return render(request, 'pages/account.html',{"user":user, "alert_message":alert_message})
        
def change_password(request):
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        current_password=request.POST["current_password"]
        new_password=request.POST["new_password"]
        new_password2=request.POST["new_password2"]
        if user.check_password(current_password)==False:
            alert_message="Current password is incorrect!"
            return render(request, 'pages/change-password.html',{"alert_message":alert_message})
        else: 
            if new_password==current_password:
                alert_message="New password cannot be the same as the current password!"
                return render(request, 'pages/change-password.html',{"alert_message":alert_message})
            elif validate_password(new_password)==False:
                alert_message="Password must be at least 8 characters long and must contain at least one letter and one number!"
                return render(request, 'pages/change-password.html',{"alert_message":alert_message})
            elif new_password!=new_password2:
                alert_message="Passwords do not match!"
                return render(request, 'pages/change-password.html',{"alert_message":alert_message})
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully!")
                return redirect('/logout')
    if request.method=="GET":
        return render(request, 'pages/change-password.html',{})
