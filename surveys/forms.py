from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Response, Answer, Question, Survey
import json
from django.utils import timezone

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'visibility', 'access_password', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        error_messages = {
            'title': {
                'required': 'Please provide a title for your survey.',
                'max_length': 'The title is too long. Maximum length is 200 characters.'
            },
            'description': {
                'max_length': 'The description is too long.'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        visibility = cleaned_data.get('visibility')
        access_password = cleaned_data.get('access_password')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError({
                    'end_date': 'End date must be after start date.'
                })
            if start_date < timezone.now():
                raise ValidationError({
                    'start_date': 'Start date cannot be in the past.'
                })

        if visibility == 'password_protected':
            if not access_password:
                raise ValidationError({
                    'access_password': 'Password is required for password-protected surveys.'
                })
            elif len(access_password) < 6:
                raise ValidationError({
                    'access_password': 'Password must be at least 6 characters long.'
                })

        return cleaned_data

class QuestionForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'placeholder': 'Enter options, one per line (for choice questions)'
        }),
        required=False
    )

    class Meta:
        model = Question
        fields = ['text', 'question_type', 'is_required', 'order', 'options']
        error_messages = {
            'text': {
                'required': 'Question text is required.',
                'max_length': 'Question text is too long.'
            },
            'order': {
                'required': 'Question order is required.',
                'invalid': 'Please enter a valid number for question order.'
            }
        }

    def clean_options(self):
        question_type = self.cleaned_data.get('question_type')
        options = self.cleaned_data.get('options', '').strip()

        if question_type in ['single_choice', 'multiple_choice']:
            if not options:
                raise ValidationError('Options are required for choice questions.')
            
            # Split options by newline and filter empty lines
            option_list = [opt.strip() for opt in options.split('\n') if opt.strip()]
            
            if len(option_list) < 2:
                raise ValidationError('At least two options are required for choice questions.')
            elif len(option_list) > 10:
                raise ValidationError('Maximum 10 options are allowed per question.')
            
            # Check for duplicate options
            if len(option_list) != len(set(option_list)):
                raise ValidationError('Duplicate options are not allowed.')
                
            return option_list
        elif question_type == 'rating':
            return list(range(1, 6))  # 1-5 rating
        elif question_type == 'yes_no':
            return ['Yes', 'No']
        
        return None

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        text = cleaned_data.get('text', '').strip()

        if not text:
            raise ValidationError({
                'text': 'Question text cannot be empty.'
            })

        if len(text) > 500:
            raise ValidationError({
                'text': 'Question text cannot exceed 500 characters.'
            })

        return cleaned_data

QuestionFormSet = inlineformset_factory(
    Survey, Question,
    form=QuestionForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        super().__init__(*args, **kwargs)

        # Add a field for each question
        for question in self.survey.questions.all():
            field_name = f'question_{question.id}'
            
            if question.question_type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=question.text,
                    required=question.is_required,
                    widget=forms.Textarea(attrs={'rows': 3})
                )
            elif question.question_type == 'multiple_choice':
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=question.text,
                    choices=[(opt, opt) for opt in question.options],
                    widget=forms.CheckboxSelectMultiple,
                    required=question.is_required
                )
            elif question.question_type == 'single_choice':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=[(opt, opt) for opt in question.options],
                    widget=forms.RadioSelect,
                    required=question.is_required
                )
            elif question.question_type == 'rating':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=[(str(i), str(i)) for i in range(1, 6)],
                    widget=forms.RadioSelect,
                    required=question.is_required
                )
            elif question.question_type == 'yes_no':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=[('Yes', 'Yes'), ('No', 'No')],
                    widget=forms.RadioSelect,
                    required=question.is_required
                )

    def save(self, commit=True):
        response = super().save(commit=False)
        response.survey = self.survey
        
        if commit:
            response.save()
            # Create Answer objects for each question
            for question in self.survey.questions.all():
                field_name = f'question_{question.id}'
                if field_name in self.cleaned_data:
                    answer_value = self.cleaned_data[field_name]
                    # Convert lists to JSON for storage
                    if isinstance(answer_value, (list, tuple)):
                        answer_value = json.dumps(answer_value)
                    Answer.objects.create(
                        response=response,
                        question=question,
                        answer_value=answer_value
                    )
        return response