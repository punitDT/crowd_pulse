import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from surveys.models import Survey, Question, Response, Answer
from django.utils.text import slugify

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crowd_pulse.settings')
django.setup()

def create_users():
    users = []
    usernames = ['survey_admin', 'researcher', 'teacher', 'student', 'business_analyst']
    for i, username in enumerate(usernames):
        email = f'{username}@example.com'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_active': True
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"Created user: {username} (password: test123)")
        users.append(user)
    return users

def create_surveys(users):
    surveys = []
    survey_data = [
        {
            'title': "Customer Satisfaction Survey",
            'description': "Help us improve our services by sharing your feedback",
            'visibility': 'public',
            'questions': [
                {
                    'text': "How satisfied are you with our service?",
                    'type': 'single_choice',
                    'options': ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
                    'is_required': True
                },
                {
                    'text': "Rate our customer support (1-5)",
                    'type': 'rating',
                    'is_required': True,
                    'options': list(range(1, 6))
                },
                {
                    'text': "What improvements would you suggest?",
                    'type': 'text',
                    'is_required': False
                }
            ],
            'settings': {
                'is_public': True,
                'allow_anonymous': True,
                'end_date': datetime(2025, 4, 9)
            }
        },
        {
            'title': "Event Registration Form",
            'description': "Register for our annual tech conference",
            'visibility': 'private',
            'questions': [
                {
                    'text': "Full Name",
                    'type': 'text',
                    'is_required': True
                },
                {
                    'text': "T-Shirt Size",
                    'type': 'single_choice',
                    'options': ["XS", "S", "M", "L", "XL", "XXL"],
                    'is_required': True
                },
                {
                    'text': "Which sessions would you like to attend?",
                    'type': 'multiple_choice',
                    'options': ["AI/ML Workshop", "Cloud Computing", "Web Development", "Mobile Development", "DevOps"],
                    'is_required': True
                }
            ],
            'settings': {
                'is_public': False,
                'requires_login': True,
                'max_responses': 200
            }
        },
        {
            'title': "Employee Engagement Survey",
            'description': "Anonymous survey to improve workplace culture",
            'visibility': 'private',
            'questions': [
                {
                    'text': "Rate the following aspects: Work-life balance",
                    'type': 'single_choice',
                    'options': ["Poor", "Fair", "Good", "Excellent"],
                    'is_required': True
                },
                {
                    'text': "Rate the following aspects: Career growth",
                    'type': 'single_choice',
                    'options': ["Poor", "Fair", "Good", "Excellent"],
                    'is_required': True
                },
                {
                    'text': "Rate the following aspects: Team collaboration",
                    'type': 'single_choice',
                    'options': ["Poor", "Fair", "Good", "Excellent"],
                    'is_required': True
                },
                {
                    'text': "Rate the following aspects: Management support",
                    'type': 'single_choice',
                    'options': ["Poor", "Fair", "Good", "Excellent"],
                    'is_required': True
                },
                {
                    'text': "Rank these benefits (1 being most important): Health insurance, Remote work, Professional development, Retirement plans, Paid time off",
                    'type': 'text',
                    'is_required': True
                }
            ],
            'settings': {
                'is_public': False,
                'allow_anonymous': True,
                'prevent_multiple_submissions': True
            }
        }
    ]
    
    for data in survey_data:
        creator = random.choice(users)
        settings = data.get('settings', {})
        
        survey = Survey.objects.create(
            title=data['title'],
            description=data['description'],
            creator=creator,
            slug=slugify(data['title']),
            visibility=data['visibility'],
            is_active=True,
            start_date=timezone.now(),
            end_date=settings.get('end_date', timezone.now() + timedelta(days=30))
        )
        
        # Create questions for this survey
        for i, q in enumerate(data['questions'], 1):
            Question.objects.create(
                survey=survey,
                text=q['text'],
                question_type=q['type'],
                is_required=q.get('is_required', True),
                order=i,
                options=q.get('options', None)
            )
        
        surveys.append(survey)
        print(f"Created survey: {data['title']}")
    return surveys

def create_responses(surveys, users):
    for survey in surveys:
        questions = survey.questions.all()
        for _ in range(5):  # 5 responses per survey
            respondent = random.choice(users)
            response = Response.objects.create(
                survey=survey,
                respondent=respondent,
                completed_at=timezone.now(),
                ip_address='127.0.0.1'
            )
            
            for question in questions:
                answer_value = None
                if question.question_type == 'multiple_choice':
                    answer_value = random.sample(question.options, random.randint(1, len(question.options)))
                elif question.question_type == 'single_choice':
                    answer_value = random.choice(question.options)
                elif question.question_type == 'text':
                    answer_value = f"Sample feedback for {survey.title}"
                elif question.question_type == 'rating':
                    answer_value = random.randint(1, 5)
                elif question.question_type == 'yes_no':
                    answer_value = random.choice(['Yes', 'No'])
                
                Answer.objects.create(
                    response=response,
                    question=question,
                    answer_value=answer_value
                )
        print(f"Created {5} responses for survey: {survey.title}")

def main():
    print("Creating dummy data...")
    print("\n1. Creating users...")
    users = create_users()
    
    print("\n2. Creating surveys with questions...")
    surveys = create_surveys(users)
    
    print("\n3. Creating survey responses...")
    create_responses(surveys, users)
    
    print("\nDummy data creation completed!")
    print("\nYou can now log in with any of these users (password: test123):")
    print("- survey_admin@example.com")
    print("- researcher@example.com")
    print("- teacher@example.com")
    print("- student@example.com")
    print("- business_analyst@example.com")

if __name__ == '__main__':
    main()