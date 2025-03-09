from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.forms.utils import ErrorDict
from .models import Survey, Question, Response, Answer
from .forms import SurveyForm, QuestionFormSet, ResponseForm

class HomeView(TemplateView):
    template_name = 'surveys/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['recent_surveys'] = Survey.objects.filter(
                visibility='public',
                is_active=True
            ).order_by('-created_at')[:6]
        except Exception as e:
            messages.error(self.request, 'Error loading recent surveys. Please try again later.')
        return context

class MySurveysView(LoginRequiredMixin, TemplateView):
    template_name = 'surveys/my_surveys.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['surveys'] = Survey.objects.filter(creator=self.request.user).order_by('-created_at')
        except Exception as e:
            messages.error(self.request, 'Error loading your surveys. Please try again later.')
        return context

class CreateSurveyView(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/create_survey.html'
    success_url = reverse_lazy('my_surveys')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'title': "Customer Satisfaction Survey",
            'description': "Help us improve our services by sharing your feedback",
            'visibility': 'public',
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=365)
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['question_formset'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            initial_questions = [
                {
                    'text': "How satisfied are you with our service?",
                    'question_type': 'single_choice',
                    'is_required': True,
                    'order': 1,
                    'options': "Very Satisfied\nSatisfied\nNeutral\nDissatisfied\nVery Dissatisfied"
                },
                {
                    'text': "Rate our customer support (1-5)",
                    'question_type': 'rating',
                    'is_required': True,
                    'order': 2,
                },
                {
                    'text': "What improvements would you suggest?",
                    'question_type': 'text',
                    'is_required': False,
                    'order': 3,
                }
            ]
            context['question_formset'] = QuestionFormSet(
                instance=self.object,
                initial=initial_questions,
                extra=max(0, 3 - len(initial_questions))
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        question_formset = context['question_formset']
        
        try:
            if question_formset.is_valid():
                self.object = form.save(commit=False)
                self.object.creator = self.request.user
                self.object.save()
                question_formset.instance = self.object
                question_formset.save()
                messages.success(self.request, 'Survey created successfully!')
                return super().form_valid(form)
            else:
                # Handle formset errors
                error_messages = []
                for form_errors in question_formset.errors:
                    for field, errors in form_errors.items():
                        error_messages.extend(errors)
                if error_messages:
                    messages.error(self.request, 'Question errors: ' + ' '.join(error_messages))
                return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error creating survey: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        # Add form-specific error messages
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        
        try:
            # Check if survey is accessible
            if not survey.is_active:
                messages.warning(self.request, 'This survey is no longer active.')
            elif survey.end_date and survey.end_date < timezone.now():
                messages.warning(self.request, 'This survey has ended.')
            elif survey.start_date and survey.start_date > timezone.now():
                messages.info(self.request, f'This survey will start on {survey.start_date.strftime("%B %d, %Y at %I:%M %p")}')
        except Exception as e:
            messages.error(self.request, 'Error loading survey details. Please try again later.')
            
        return context

class StartSurveyView(FormView):
    template_name = 'surveys/start_survey.html'
    form_class = ResponseForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.survey = get_object_or_404(Survey, slug=self.kwargs['slug'])
            if not self.survey.is_active:
                messages.error(request, 'This survey is no longer active.')
                return redirect('survey_detail', slug=self.survey.slug)
            if self.survey.end_date and self.survey.end_date < timezone.now():
                messages.error(request, 'This survey has ended.')
                return redirect('survey_detail', slug=self.survey.slug)
            if self.survey.start_date and self.survey.start_date > timezone.now():
                messages.error(request, 'This survey has not started yet.')
                return redirect('survey_detail', slug=self.survey.slug)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, 'Error accessing survey. Please try again later.')
            return redirect('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = self.survey
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = self.survey
        return context

    def form_valid(self, form):
        try:
            response = form.save(commit=False)
            response.survey = self.survey
            response.respondent = self.request.user if self.request.user.is_authenticated else None
            response.ip_address = self.request.META.get('REMOTE_ADDR')
            response.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
            response.completed_at = timezone.now()
            response.save()
            
            messages.success(self.request, 'Thank you for completing the survey!')
            return redirect('survey_detail', slug=self.survey.slug)
        except Exception as e:
            messages.error(self.request, 'Error submitting response. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        # Add field-specific error messages
        for field, errors in form.errors.items():
            for error in errors:
                # Get the question text instead of field name for better error messages
                field_name = field.replace('question_', '')
                try:
                    question = self.survey.questions.get(id=field_name)
                    messages.error(self.request, f'"{question.text}": {error}')
                except:
                    messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)
