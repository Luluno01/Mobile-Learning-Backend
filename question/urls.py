from django.urls import path, re_path, include

from . import views

app_name = 'question'
urlpatterns = [
    # One-choice question
    re_path(r'^one-choice-question/list/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getSimpleList),
    re_path(r'^one-choice-question/id-list/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getIdList),
    path('one-choice-question/simple/<int:question>/', views.OneChoiceQuestionView.getSimpleQuestionInfo),
    path('one-choice-question/full/<int:question>/', views.OneChoiceQuestionView.getFullQuestionInfo),
    re_path(r'^one-choice-question/search/((?P<categories>\[[ %,\d]*?\])/)?((?P<topics>\[[\s\S]*?\])/)?((?P<question_text>[\s\S]*?)/)?', views.OneChoiceQuestionView.search),
    re_path(r'^one-choice-question/new/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getNew),
    re_path(r'^one-choice-question/hot/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getHot),
    re_path(r'^one-choice-question/validate/((?P<question>\d+)/)?((?P<answer>\d+)/)?$', views.OneChoiceQuestionView.validate),
    # Fill-in-the-blank question
    re_path(r'^fill-in-question/list/((?P<category>\d+)/)?$', views.FillInQuestionView.getSimpleList),
    re_path(r'^fill-in-question/id-list/((?P<category>\d+)/)?$', views.FillInQuestionView.getIdList),
    path('fill-in-question/simple/<int:question>/', views.FillInQuestionView.getSimpleQuestionInfo),
    path('fill-in-question/full/<int:question>/', views.FillInQuestionView.getFullQuestionInfo),
    re_path(r'^fill-in-question/search/((?P<categories>\[[ %,\d]*?\])/)?((?P<topics>\[[\s\S]*?\])/)?((?P<question_text>[\s\S]*?)/)?', views.FillInQuestionView.search),
    re_path(r'^fill-in-question/new/((?P<category>\d+)/)?$', views.FillInQuestionView.getNew),
    re_path(r'^fill-in-question/hot/((?P<category>\d+)/)?$', views.FillInQuestionView.getHot),
    re_path(r'^fill-in-question/validate/((?P<question>\d+)/)?$', views.FillInQuestionView.validate),
    # Subjective question
    re_path(r'^subjective-question/list/((?P<category>\d+)/)?$', views.SubjectiveQuestionView.getSimpleList),
    re_path(r'^subjective-question/id-list/((?P<category>\d+)/)?$', views.SubjectiveQuestionView.getIdList),
    path('subjective-question/simple/<int:question>/', views.SubjectiveQuestionView.getSimpleQuestionInfo),
    path('subjective-question/full/<int:question>/', views.SubjectiveQuestionView.getFullQuestionInfo),
    re_path(r'^subjective-question/search/((?P<categories>\[[ %,\d]*?\])/)?((?P<topics>\[[\s\S]*?\])/)?((?P<question_text>[\s\S]*?)/)?', views.SubjectiveQuestionView.search),
    re_path(r'^subjective-question/new/((?P<category>\d+)/)?$', views.SubjectiveQuestionView.getNew),
    re_path(r'^subjective-question/hot/((?P<category>\d+)/)?$', views.SubjectiveQuestionView.getHot),
    re_path(r'^subjective-question/validate/((?P<question>\d+)/)?$', views.SubjectiveQuestionView.validate),
    # True-or-false question
    re_path(r'^true-or-false-question/list/((?P<category>\d+)/)?$', views.TrueOrFalseQuestionView.getSimpleList),
    re_path(r'^true-or-false-question/id-list/((?P<category>\d+)/)?$', views.TrueOrFalseQuestionView.getIdList),
    path('true-or-false-question/simple/<int:question>/', views.TrueOrFalseQuestionView.getSimpleQuestionInfo),
    path('true-or-false-question/full/<int:question>/', views.TrueOrFalseQuestionView.getFullQuestionInfo),
    re_path(r'^true-or-false-question/search/((?P<categories>\[[ %,\d]*?\])/)?((?P<topics>\[[\s\S]*?\])/)?((?P<question_text>[\s\S]*?)/)?', views.TrueOrFalseQuestionView.search),
    re_path(r'^true-or-false-question/new/((?P<category>\d+)/)?$', views.TrueOrFalseQuestionView.getNew),
    re_path(r'^true-or-false-question/hot/((?P<category>\d+)/)?$', views.TrueOrFalseQuestionView.getHot),
    re_path(r'^true-or-false-question/validate/((?P<question>\d+)/)?((?P<answer>true|false|True|False|0)/)?$', views.TrueOrFalseQuestionView.validate),
    # Multiple-choice question
    re_path(r'^multiple-choice-question/list/((?P<category>\d+)/)?$', views.MultipleChoiceQuestionView.getSimpleList),
    re_path(r'^multiple-choice-question/id-list/((?P<category>\d+)/)?$', views.MultipleChoiceQuestionView.getIdList),
    path('multiple-choice-question/simple/<int:question>/', views.MultipleChoiceQuestionView.getSimpleQuestionInfo),
    path('multiple-choice-question/full/<int:question>/', views.MultipleChoiceQuestionView.getFullQuestionInfo),
    re_path(r'^multiple-choice-question/search/((?P<categories>\[[ %,\d]*?\])/)?((?P<topics>\[[\s\S]*?\])/)?((?P<question_text>[\s\S]*?)/)?', views.MultipleChoiceQuestionView.search),
    re_path(r'^multiple-choice-question/new/((?P<category>\d+)/)?$', views.MultipleChoiceQuestionView.getNew),
    re_path(r'^multiple-choice-question/hot/((?P<category>\d+)/)?$', views.MultipleChoiceQuestionView.getHot),
    re_path(r'^multiple-choice-question/validate/((?P<question>\d+)/)?((?P<answer>\[[ %,\d]*?\])/)?$', views.MultipleChoiceQuestionView.validate)
]