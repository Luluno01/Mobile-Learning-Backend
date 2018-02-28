from django.contrib.postgres.fields import ArrayField
from django.db import models
from .Question import Question

def __defaultList__():
    return []

class FillInQuestion(Question):
    '''Fill-in-the-blank question
    '''
    answer = ArrayField(models.CharField(max_length=100, default=''), default=__defaultList__)  # Answers of this question