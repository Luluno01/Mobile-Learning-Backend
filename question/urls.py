from django.urls import path, re_path, include

from . import views

app_name = 'question'
urlpatterns = [
    re_path(r'^one-choice-question/list/((?P<category>\d+)/)?$', views.OneChoiceQuestionView.getSimpleList),
    path('one-choice-question/simple/<int:question>/', views.OneChoiceQuestionView.getSimpleQuestionInfo),
    path('one-choice-question/full/<int:question>/', views.OneChoiceQuestionView.getFullQuestionInfo),
    path('one-choice-question/validate/<int:question>/<int:answer>/', views.OneChoiceQuestionView.validate)
]