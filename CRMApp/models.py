from django.db import models
from django.contrib.auth.models import User


# Create your models here.
   
class Contact(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50, default="")
    organization_name=models.CharField(max_length=250, default="")
    organization=models.BooleanField(default=False)
    email=models.EmailField()
    phone=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    notes=models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
      
class Pipeline(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contact=models.ForeignKey(Contact, on_delete=models.CASCADE)
    stage=models.CharField(max_length=50)
    notes=models.TextField()    

    def __str__(self):
        return self.contact.first_name
    

class Event(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contact=models.ForeignKey(Contact, on_delete=models.CASCADE)
    event_name=models.CharField(max_length=100)
    event_date=models.DateField()
    event_time=models.TimeField()
    event_location=models.CharField(max_length=100)
    event_description=models.TextField()
    done=models.BooleanField(default=False)

    def __str__(self):
        return self.event_name