from django.db import models
from .Questions.OneChoiceQuestion import OneChoiceQuestion, OneChoiceChoice
from .Questions.FillInQuestion import FillInQuestion
from .Questions.SubjectiveQuestion import SubjectiveQuestion
from .Questions.TrueOrFalseQuestion import TrueOrFalseQuestion
from .Questions.MultipleChoiceQuestion import MultipleChoiceQuestion, MultipleChoiceChoice

# Create your models here.

OneChoiceQuestion = OneChoiceQuestion
OneChoiceChoice = OneChoiceChoice
FillInQuestion = FillInQuestion
SubjectiveQuestion = SubjectiveQuestion
TrueOrFalseQuestion = TrueOrFalseQuestion
MultipleChoiceQuestion = MultipleChoiceQuestion
MultipleChoiceChoice = MultipleChoiceChoice