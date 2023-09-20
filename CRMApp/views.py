from django.shortcuts import render
from .models import Pipeline

# Create your views here.
def add_pipeline(request):
    if request.method== "POST":
        lead=request.POST["lead"]
        stage=request.POST["stage"]
        notes=request.POST["notes"]
        due_date=request.POST["dueDate"]
        event=request.POST["event"]
        
        new_pipeline=Pipeline(lead=lead, stage=stage, notes=notes, due_dates=due_date, event=event)
        new_pipeline.save()
        
        
        
    return render(request, 'pages/add-pipeline.html',{})

def base(request):
    return render(request, 'base.html',{})