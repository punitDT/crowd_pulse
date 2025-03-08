from django.shortcuts import render
from django.views.generic import TemplateView
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
