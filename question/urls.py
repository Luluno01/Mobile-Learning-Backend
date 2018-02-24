from django.urls import path, re_path, include

from . import views

app_name = 'question'
urlpatterns = [
    # One-choice question
    re_path(r'^one-choice-question/list/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getSimpleList),
    path('one-choice-question/simple/<int:question>/', views.OneChoiceQuestionView.getSimpleQuestionInfo),
    path('one-choice-question/full/<int:question>/', views.OneChoiceQuestionView.getFullQuestionInfo),
    re_path(r'one-choice-question/validate/((?P<question>\d+)/)?((?P<answer>\d+)/)?$', views.OneChoiceQuestionView.validate),
    # Fill-in-the-blank question
    re_path(r'^fill-in-question/list/((?P<category>\d+)/)?$', views.FillInQuestionView.getSimpleList),
    path('fill-in-question/simple/<int:question>/', views.FillInQuestionView.getSimpleQuestionInfo),
    path('fill-in-question/full/<int:question>/', views.FillInQuestionView.getFullQuestionInfo),
    re_path(r'fill-in-question/validate/((?P<question>\d+)/)?$', views.FillInQuestionView.validate),
    # Subjective question
    re_path(r'^subjective-question/list/((?P<category>\d+)/)?$', views.SubjectiveQuestionView.getSimpleList),
    path('subjective-question/simple/<int:question>/', views.SubjectiveQuestionView.getSimpleQuestionInfo),
    path('subjective-question/full/<int:question>/', views.SubjectiveQuestionView.getFullQuestionInfo),
    re_path(r'subjective-question/validate/((?P<question>\d+)/)?$', views.SubjectiveQuestionView.validate),
    # True-or-false question
    re_path(r'^true-or-false-question/list/((?P<category>\d+)/)?$', views.TrueOrFalseQuestionView.getSimpleList),
    path('true-or-false-question/simple/<int:question>/', views.TrueOrFalseQuestionView.getSimpleQuestionInfo),
    path('true-or-false-question/full/<int:question>/', views.TrueOrFalseQuestionView.getFullQuestionInfo),
    re_path(r'true-or-false-question/validate/((?P<question>\d+)/)?((?P<answer>true|false|True|False)/)?$', views.TrueOrFalseQuestionView.validate)
]