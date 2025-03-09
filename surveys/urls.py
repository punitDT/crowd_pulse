from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSurveyView.as_view(), name='create_survey'),
    path('my-surveys/', views.MySurveysView.as_view(), name='my_surveys'),
    path('<slug:slug>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    path('<slug:slug>/start/', views.StartSurveyView.as_view(), name='start_survey'),
]