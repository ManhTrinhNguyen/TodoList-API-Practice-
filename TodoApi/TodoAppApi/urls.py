from django.urls import path
from . import views
urlpatterns = [
  path('tasks', views.tasks),
  path('task/<int:pk>', views.task)
]