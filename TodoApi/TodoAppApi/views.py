from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Task 
import json

# Create your views here.

@csrf_exempt
def tasks(request):
  if request.method == 'GET':
    tasks = Task.objects.all().values()
    return JsonResponse({'tasks': list(tasks)})
  elif request.method == 'POST':
# Parse JSON data
    try:
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        completed = data.get('completed')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Ensure all fields are present
    if not title or not description or completed is None:
        return JsonResponse({
            'error': 'True',
            'message': 'Missing field required'
        }, status=400)

    # Create and save the Task
    task = Task(title=title, description=description, completed=completed)
    try:
        task.save()
    except IntegrityError:
        return JsonResponse({
            'error': 'True',
            'message': 'Database error'
        }, status=400)
    
    return JsonResponse(model_to_dict(task), status=201)
  
@csrf_exempt
def task(request, pk):
   try:
      task = Task.objects.get(id = pk)
   except: 
      return JsonResponse({'error': 'Task not Found'}, status = 404)
   
   if request.method == 'GET':
      return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
   elif request.method == 'PUT':
      data = json.loads(request.body)
      task.title = data.get('title', task.title)
      task.description = data.get('description', task.description)
      task.completed = data.get('completed', task.completed)
      task.save()
      return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}, status = 200)
   elif request.method == 'DELETE':
      task.delete()
      return HttpResponse(status=204)
