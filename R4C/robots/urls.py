from django.urls import path

from .views import index, new_robot_record, download_excel


urlpatterns = [
    path('', index, name='home'),
    path('create/', new_robot_record, name='new_robot_record'),
    path('excel/', download_excel, name='download_excel'),
]