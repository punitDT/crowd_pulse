from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Survey

class HomeView(TemplateView):
    template_name = 'surveys/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_surveys'] = Survey.objects.filter(
            visibility='public',
            is_active=True
        ).order_by('-created_at')[:6]
        return context

class CreateSurveyView(LoginRequiredMixin, CreateView):
    model = Survey
    template_name = 'surveys/create_survey.html'
    fields = ['title', 'description', 'visibility', 'access_password', 'start_date', 'end_date']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
