from django.db import models
from .Question import Question

def __defaultList__():
    return []

class SubjectiveQuestion(Question):
    '''Subjective question
    '''
    answer = models.TextField(default='')  # Answer of this question