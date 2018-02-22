from django.db import models
from .Question import Question
from django.db.models import F
import logging
logger = logging.getLogger("django")

class ChoiceQuestion(Question):
    '''Base class for choice question
    '''
    accuracy = models.FloatField(default=0)  # Accuracy

class Choice(models.Model):
    '''Base class for choices
    '''
    # question = models.ForeignKey(ChoiceQuestion, models.CASCADE, null=False)
    choice_text = models.TextField(default='')
    selection_count = models.IntegerField(default=0)

    @property
    def choice_id(self):
        return self.id + 0

    @classmethod
    def clearNoOwner(cls):
        logger.warning('Clearing choices belong to no question')
        cls.objects.filter(question=None).delete()

    def toJson(self):
        return {
            'id': self.id,
            'choice_text': self.choice_text,
            'selection_count': self.selection_count
        }

    def countInc(self):
        self.selection_count = F('selection_count') + 1
        self.save()

    def __str__(self):
        return self.choice_text