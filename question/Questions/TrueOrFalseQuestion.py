from django.db import models
from django.db.models import F
from .Question import Question

class TrueOrFalseQuestion(Question):
    '''True-or-false question
    '''
    answer = models.BooleanField(default=True)  # Answer of this question
    correct_count = models.IntegerField(default=0)

    def toSimpleJson(self):
        '''Return simply serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            'category': self.category,
            'topic': self.topic,
            'accuracy': self.accuracy(),
            'visit_count': self.visit_count,
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
            'accuracy': self.accuracy(),
            'visit_count': self.visit_count,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def validate(self, usersAnswer, *args, **kwargs):
        if type(usersAnswer) != bool:
            raise ValueError('Invalid answer type')
        self.visit_count = F('visit_count') + 1
        if self.answer == usersAnswer:
            self.correct_count = F('correct_count') + 1
        self.save()

    def accuracy(self):
        if self.visit_count:
            return self.correct_count / self.visit_count
        else:
            return 0