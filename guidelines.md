# Cursor AI Guidelines for Crowd Pulse

## Overview

This document provides guidelines for implementing Cursor AI within the Crowd Pulse Live Polling & Survey Platform. Cursor AI will enhance user experience through intelligent assistance, predictive features, and automated optimizations.

## Core Principles

1. **User-Centered Design**: All AI implementations should prioritize user experience and reduce friction in the poll/survey creation process.
2. **Progressive Enhancement**: AI features should enhance existing functionality without disrupting core platform operations.
3. **Transparent Operation**: Users should understand when and how AI is assisting them.
4. **Data Privacy**: All AI operations must comply with privacy settings and data protection regulations.

## Tech Stack Documentation

### Core Technologies
- **Django**: [Official Documentation](https://docs.djangoproject.com/en/stable/)
  - Django REST Framework: [Documentation](https://www.django-rest-framework.org/)
  - Django Channels (for WebSockets): [Documentation](https://channels.readthedocs.io/en/stable/)

- **PostgreSQL**: [Official Documentation](https://www.postgresql.org/docs/)
  - psycopg2 (Python adapter): [Documentation](https://www.psycopg.org/docs/)
  - Django PostgreSQL features: [Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/)

- **Authentication**:
  - Google Sign-In: [Integration Guide](https://developers.google.com/identity/sign-in/web/sign-in)
  - Django Social Auth: [Documentation](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
  - django-allauth: [Documentation](https://django-allauth.readthedocs.io/en/latest/installation.html)

- **AI Integration**:
  - Django ML: [Documentation](https://django-ml.readthedocs.io/)
  - OpenAI API: [Documentation](https://platform.openai.com/docs/api-reference)
  - TensorFlow Serving: [Documentation](https://www.tensorflow.org/tfx/guide/serving)

### Frontend Technologies
- **React**: [Documentation](https://reactjs.org/docs/getting-started.html)
- **Chart.js**: [Documentation](https://www.chartjs.org/docs/latest/)
- **Socket.io Client**: [Documentation](https://socket.io/docs/v4/client-api/)

### Deployment & DevOps
- **Docker**: [Documentation](https://docs.docker.com/)
- **Django with PostgreSQL Deployment**: [Guide](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- **Nginx Configuration**: [Documentation](https://nginx.org/en/docs/)

## Implementation Areas

### 1. Poll/Survey Creation Assistant

- **Smart Templates**: Analyze user intent and suggest appropriate poll/survey templates based on stated goals.
- **Question Optimization**: Analyze draft questions and suggest improvements for clarity, neutrality, and engagement.
- **Response Option Generation**: Suggest comprehensive answer choices based on question content.
- **Survey Flow Optimization**: Recommend optimal question ordering and branching logic.

### 2. Predictive Analytics

- **Response Prediction**: Estimate potential response rates and demographics based on distribution method and content.
- **Completion Time Estimates**: Calculate estimated completion time for respondents.
- **Drop-off Point Prediction**: Identify questions that may cause respondent abandonment.
- **Outcome Projections**: Project potential results based on similar historical polls/surveys.

### 3. Automated Content Enhancement

- **Image Suggestions**: Recommend relevant images for questions based on content.
- **Language Optimization**: Suggest wording improvements for better engagement and reduced bias.
- **Accessibility Checks**: Automatically scan for and suggest improvements for accessibility.
- **Multi-language Support**: Provide intelligent translation suggestions with context awareness.

### 4. Real-time Adaptation

- **Dynamic Question Adjustment**: Modify subsequent questions based on incoming response patterns.
- **Engagement Boosting**: Suggest modifications to increase completion rates during live polls.
- **Anomaly Detection**: Flag unusual response patterns that may indicate spam or manipulation.
- **Respondent Assistance**: Provide context-aware help for respondents who appear confused.

### 5. Results Interpretation

- **Automated Insights**: Generate natural language summaries of poll/survey results.
- **Correlation Discovery**: Identify meaningful correlations between different response data.
- **Sentiment Analysis**: Analyze text responses for sentiment and key themes.
- **Comparative Analysis**: Automatically compare results to industry benchmarks or previous polls.

## Technical Implementation Guidelines

### AI Model Selection

- Use **GPT-4** or equivalent for natural language understanding and generation tasks.
- Implement **BERT** derivatives for classification and sentiment analysis.
- Utilize **Recommendation Systems** for template and option suggestions.

### Database Schema Considerations

- Design schema to efficiently store AI-generated suggestions separately from user content
- Create appropriate PostgreSQL indexes for queries commonly used by AI components
- Implement JSON field types for flexible storage of AI analysis results
- Consider partitioning for large-scale response data to improve query performance

### Integration Points

1. **Frontend Components**:
   - Embed AI suggestions within the poll creation interface using non-intrusive tooltips.
   - Implement a dedicated "AI Assistant" panel that can be expanded/collapsed.

2. **Backend Processing**:
   - Process surveys through AI analysis pipeline before saving.
   - Run periodic batch analysis on existing surveys to generate improvement suggestions.

3. **API Architecture**:
   - Create a dedicated AI microservice with standardized request/response patterns.
   - Implement rate limiting to prevent abuse of AI-intensive operations.

### Google Sign-In Implementation

- Use django-allauth for handling OAuth2 authentication flow
- Configure proper callback URLs in Google Cloud Console
- Implement appropriate user profile creation on first sign-in
- Store minimal required user data to comply with privacy regulations
- Consider JWT-based authentication for API interactions post sign-in

### Performance Considerations

- Cache common AI-generated suggestions to reduce processing time.
- Implement progressive loading for AI features to maintain responsiveness.
- Offer "AI-light" mode for users with performance concerns.
- Use PostgreSQL's advanced indexing features for optimizing AI-related queries
- Consider read replicas for analytics-heavy operations

## User Experience Guidelines

### Discoverability

- Introduce AI capabilities through an optional onboarding tour.
- Use subtle indicators to show where AI assistance is available.
- Provide an AI features overview in the help documentation.

### Control

- Allow users to accept/reject/modify all AI suggestions.
- Implement confidence indicators for AI recommendations.
- Provide an option to disable specific AI features.

### Feedback Loop

- Collect user feedback on AI suggestions to improve accuracy.
- Track acceptance rates of different AI feature categories.
- Implement A/B testing for different AI interaction patterns.

## Ethical Considerations

### Bias Prevention

- Regularly audit AI suggestions for potential bias.
- Implement diversity in training data to ensure fairness.
- Provide bias warnings for potentially problematic questions.

### Transparency

- Clearly mark AI-generated content and suggestions.
- Explain the basis for AI recommendations when appropriate.
- Provide methodology documentation for how AI analyzes responses.

### Data Usage

- Limit AI training on user data to explicit opt-in scenarios.
- Anonymize all data used for improving AI capabilities.
- Establish clear retention policies for AI-processed data.

## Implementation Roadmap

### Phase 1: Foundation
- Implement basic question improvement suggestions
- Add template recommendations
- Deploy simple response analysis
- Set up Google Sign-In integration

### Phase 2: Enhancement
- Add predictive analytics features
- Implement real-time response optimization
- Deploy intelligent branching logic
- Expand PostgreSQL optimizations for scale

### Phase 3: Advanced Features
- Integrate sentiment analysis for open responses
- Add automated insight generation
- Implement cross-survey intelligence
- Deploy advanced caching strategies

## Evaluation Metrics

- **Suggestion Acceptance Rate**: Percentage of AI suggestions implemented by users
- **Time Savings**: Reduction in poll/survey creation time
- **Completion Rate Improvement**: Increase in survey completion rates
- **User Satisfaction**: Feedback scores for AI-assisted features
- **Insight Value**: User ratings of AI-generated insights
- **Authentication Success Rate**: Percentage of successful Google Sign-In completions

## Conclusion

When properly implemented, Cursor AI will transform Crowd Pulse from a simple polling platform into an intelligent research assistant that helps users create more effective surveys, gather better data, and extract more valuable insights.
