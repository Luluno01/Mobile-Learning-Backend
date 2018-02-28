from django.db import models
from .Questions.OneChoiceQuestion import OneChoiceQuestion, OneChoiceChoice
from .Questions.FillInQuestion import FillInQuestion
from .Questions.SubjectiveQuestion import SubjectiveQuestion
from .Questions.TrueOrFalseQuestion import TrueOrFalseQuestion
from .Questions.MultipleChoiceQuestion import MultipleChoiceQuestion, MultipleChoiceChoice
from .Questions.QuestionList import QuestionList

# Create your models here.

OneChoiceQuestion = OneChoiceQuestion
OneChoiceChoice = OneChoiceChoice
FillInQuestion = FillInQuestion
SubjectiveQuestion = SubjectiveQuestion
TrueOrFalseQuestion = TrueOrFalseQuestion
MultipleChoiceQuestion = MultipleChoiceQuestion
MultipleChoiceChoice = MultipleChoiceChoice
QuestionList = QuestionList

class Cron(models.Model):
    last_run = models.DateTimeField('last run time')