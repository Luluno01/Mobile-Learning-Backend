from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F
from django.utils import timezone
from enum import Enum

def __defaultList__():
    return []

class Question(models.Model):
    '''Base class for questions
    '''
    CATEGORY = Enum('Category', ('Computer Science', 'Physics', 'Math', 'Chemistry'))
    question_text = models.TextField()  # Question text
    # answer = models.IntegerField(default=0)  # Answer of this question
    resolution = models.TextField(default='')  # Resolution of this question
    category = models.IntegerField(default=1)  # Category that this question belongs to
    topic = ArrayField(models.CharField(max_length=100, default=''), default=__defaultList__)  # Involved topics of this question
    visit_count = models.IntegerField(default=0)  # Visit count of this question
    # accuracy = models.FloatField(default=0)  # Accuracy
    source = models.TextField(default='')  # Source of this question
    entry_date = models.DateTimeField('entry date')  # Entry time of this question

    @classmethod
    def create(cls, *args, **kwargs):
        '''Create a Question, or its derived question class, object
        '''
        question = cls(*args, **kwargs)
        question.entry_date = timezone.now()
        return question

    def toSimpleJson(self):
        '''Return simply serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            'category': self.category,
            'topic': self.topic,
            'visit_count': self.visit_count,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def toJson(self):
        '''Return fully serialized data of this question
        '''
        return {}

    def validate(self, usersAnswer):
        '''Validate the answer provided by a user
        '''
        pass

    def countInc(self):
        self.visit_count = F('visit_count') + 1
        self.save()

    def setCategory(self, cat):
        if type(cat) == int:
            self.category = cat
        elif type(cat) == __class__.CATEGORY:
            self.category = cat.value
        elif type(cat) == str:
            self.category = __class__.CATEGORY[cat].value
        else:
            raise TypeError('Unknown type: %s' % type(cat).__name__)

    def getCategory(self):
        return __class__.CATEGORY(self.category)

    def category_text(self):
        return self.getCategory().name
    category_text.string = True

    def question_id(self):
        return self.id + 0
    question_id.string = True

    def __str__(self):
        return self.question_text