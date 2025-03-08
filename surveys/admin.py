from django.contrib import admin
from .models import Survey, Question, Response, Answer

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'is_active', 'visibility', 'created_at')
    list_filter = ('is_active', 'visibility', 'created_at')
    search_fields = ('title', 'description', 'creator__username')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'question_type', 'is_required', 'order')
    list_filter = ('question_type', 'is_required', 'survey')
    search_fields = ('text', 'survey__title')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'respondent', 'started_at', 'completed_at')
    list_filter = ('started_at', 'completed_at')
    search_fields = ('survey__title', 'respondent__username')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question__text', 'response__survey__title')
