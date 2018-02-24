from django.contrib.postgres.fields import ArrayField
from django.db import models
from .Question import Question

def __defaultList__():
    return []

class FillInQuestion(Question):
    '''Fill-in-the-blank question
    '''
    answer = ArrayField(models.CharField(max_length=100, default=''), default=__defaultList__)  # Answers of this question

    def toJson(self):
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