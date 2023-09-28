from django.urls import path

from .views import new_robot_record


urlpatterns = [
    path('create/', new_robot_record, name='new_robot_record'),
]