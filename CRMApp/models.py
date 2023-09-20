from django.db import models


# Create your models here.
class Pipeline(models.Model):
    lead=models.CharField(max_length=50)
    stage=models.CharField(max_length=50)
    notes=models.TextField()
    due_dates=models.DateField()
    event=models.CharField(max_length=100)
    

    def __str__(self):
        return self.lead
    
