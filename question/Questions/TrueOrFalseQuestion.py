from django.db import models
from django.db.models import F
from .Question import Question

class TrueOrFalseQuestion(Question):
    '''True-or-false question
    '''
    answer = models.BooleanField(default=True)  # Answer of this question

    correct_count = models.IntegerField(default=0)
    correct_count_daily = models.IntegerField(default=0)
    correct_count_weekly = models.IntegerField(default=0)

    @property
    def accuracy(self):
        if self.visit_count:
            return self.correct_count / self.visit_count
        else:
            return 0

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

    def countResetDaily(self):
        self.visit_count_daily = 0
        self.correct_count_daily = 0

    def countResetWeekly(self):
        self.visit_count_daily = 0
        self.visit_count_weekly = 0
        self.correct_count_daily = 0
        self.correct_count_weekly = 0

    def toSimpleJson(self):
        '''Return simply serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            'category': self.category,
            'topic': self.topic,
            'accuracy': self.accuracy,
            'accuracy_daily': self.accuracy_daily,
            'accuracy_weekly': self.accuracy_weekly,
            'visit_count': self.visit_count,
            'visit_count_daily': self.visit_count_daily,
            'visit_count_weekly': self.visit_count_weekly,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def toJson(self):
        '''Return fully serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            'answer': self.answer,
            'resolution': self.resolution,
            'category': self.category,
            'topic': self.topic,
            'accuracy': self.accuracy,
            'accuracy_daily': self.accuracy_daily,
            'accuracy_weekly': self.accuracy_weekly,
            'visit_count': self.visit_count,
            'visit_count_daily': self.visit_count_daily,
            'visit_count_weekly': self.visit_count_weekly,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def validate(self, usersAnswer, *args, **kwargs):
        if type(usersAnswer) != bool:
            raise ValueError('Invalid answer type')
        self.visit_count = F('visit_count') + 1
        self.visit_count_daily = F('visit_count_daily') + 1
        self.visit_count_weekly = F('visit_count_weekly') + 1
        if self.answer == usersAnswer:
            self.correct_count = F('correct_count') + 1
            self.correct_count_daily = F('correct_count_daily') + 1
            self.correct_count_weekly = F('correct_count_weekly') + 1
        self.save()