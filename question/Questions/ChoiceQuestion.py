from django.db import models
from .Question import Question
from django.db.models import F
import logging
logger = logging.getLogger("django")

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
        return cls.objects.filter(question=None).delete()

    def toJson(self):
        return {
            'id': self.id,
            'choice_text': self.choice_text,
            'selection_count': self.selection_count
        }

    def countInc(self):
        self.selection_count = F('selection_count') + 1

    def __str__(self):
        return self.choice_text

class ChoiceQuestion(Question):
    '''Base class for choice question
    '''
    accuracy = models.FloatField(default=0)  # Accuracy

    correct_count_daily = models.IntegerField(default=0)
    correct_count_weekly = models.IntegerField(default=0)

    CHOICE_CLASS = Choice

    def countInc(self, correct=False, *args, **kwargs):
        self.visit_count = F('visit_count') + 1
        self.visit_count_daily = F('visit_count_daily') + 1
        self.visit_count_weekly = F('visit_count_weekly') + 1
        if correct:
            self.correct_count_daily = F('correct_count_daily') + 1
            self.correct_count_weekly = F('correct_count_weekly') + 1

    def countResetDaily(self):
        self.visit_count_daily = 0
        self.correct_count_daily = 0

    def countResetWeekly(self):
        self.visit_count_daily = 0
        self.visit_count_weekly = 0
        self.correct_count_daily = 0
        self.correct_count_weekly = 0

    @property
    def accuracy_daily(self):
        if self.visit_count_daily:
            return self.correct_count_daily / self.visit_count_daily
        else:
            return 0

    @property
    def accuracy_weekly(self):
        if self.visit_count_weekly:
            return self.correct_count_weekly / self.visit_count_weekly
        else:
            return 0

    def toSimpleJson(self):
        '''Return simply serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            # 'answer': self.answer,
            # 'resolution': self.resolution,
            'category': self.category,
            'topic': self.topic,
            'visit_count': self.visit_count,
            'visit_count_daily': self.visit_count_daily,
            'visit_count_weekly': self.visit_count_weekly,
            'accuracy': self.accuracy,
            'accuracy_daily': self.accuracy_daily,
            'accuracy_weekly': self.accuracy_weekly,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def toJson(self):
        '''Return fully serialized data of this question
        '''
        choices = self.CHOICE_CLASS.objects.filter(question=self)
        # answerIndex = -1
        choicesJson = []
        # for choiceIndex, choice in enumerate(choices):
        for choice in choices:
            choicesJson.append(choice.toJson())
            # if choice.id == self.answer:
            #     answerIndex = choiceIndex
        # if answerIndex == -1:
        #     logger.error('Bad question found (id: %d)' % self.id)
        return {
            'id': self.id,
            'question_text': self.question_text,
            'choices': choicesJson,
            'answer': self.answer,
            'resolution': self.resolution,
            'category': self.category,
            'topic': self.topic,
            'visit_count': self.visit_count,
            'visit_count_daily': self.visit_count_daily,
            'visit_count_weekly': self.visit_count_weekly,
            'accuracy': self.accuracy,
            'accuracy_daily': self.accuracy_daily,
            'accuracy_weekly': self.accuracy_weekly,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }