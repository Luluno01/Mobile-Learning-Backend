from django.db import models
from .Question import Question

def __defaultList__():
    return []

class SubjectiveQuestion(Question):
    '''Subjective question
    '''
    answer = models.TextField(default='')  # Answer of this question

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
            'visit_count': self.visit_count,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def validate(self, *args, **kwargs):
        self.countInc()