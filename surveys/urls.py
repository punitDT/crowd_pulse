from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSurveyView.as_view(), name='create_survey'),
]