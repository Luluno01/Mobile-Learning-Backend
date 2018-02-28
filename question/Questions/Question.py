from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from enum import Enum
import logging
logger = logging.getLogger("django")

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
    visit_count_daily = models.IntegerField(default=0)  # Visit count of this question within today
    visit_count_weekly = models.IntegerField(default=0)  # Visit count of this question within this week
    # accuracy = models.FloatField(default=0)  # Accuracy
    # accuracy_daily = models.FloatField(default=0)
    # accuracy_weekly = models.FloatField(default=0)
    
    source = models.TextField(default='')  # Source of this question
    entry_date = models.DateTimeField('entry date')  # Entry time of this question

    @classmethod
    def create(cls, *args, **kwargs):
        '''Create a Question, or its derived question class, object
        '''
        question = cls(*args, **kwargs)
        question.entry_date = timezone.now()
        return question

    @classmethod
    def search(cls, category=[], topic=[], question_text=''):
        keywords = {
            'category': None,
            'topic': None,
            'question_text': None
        }
        if category or topic or question_text:
            if category:
                keywords['category'] = Q(category=category[0])
                for index, value in enumerate(category):
                    if index > 0:
                        keywords['category'] |= Q(category=value)
            if topic:
                keywords['topic'] = Q(topic__contains=[topic[0]])
                for index, value in enumerate(topic):
                    if index > 0:
                        keywords['topic'] |= Q(topic__contains=[value])
            if question_text:
                keywords['question_text'] = Q(question_text__contains=question_text)
            condition = None
            for keyword in keywords:
                if not keywords[keyword]:
                    continue
                if not condition:
                    condition = keywords[keyword]
                else:
                    condition &= keywords[keyword]
            logger.info(cls)
            res = list(cls.objects.filter(condition))[:10]
            return list(map(lambda ques: ques.toSimpleJson(), res))
        else:
            raise ValueError('Require at least one parameter')

    @classmethod
    def getNew(cls, num=10):
        res = list(cls.objects.order_by('entry_date'))
        length = len(res)
        res = res[length - num : length]
        res.reverse()
        return list(map(lambda ques: ques.toSimpleJson(), res))

    @classmethod
    def getHot(cls, num=10):
        res = [None] * 3
        res[0] = list(cls.objects.order_by('visit_count'))
        res[1] = list(cls.objects.order_by('visit_count_daily'))
        res[2] = list(cls.objects.order_by('visit_count_weekly'))
        length = list(map(len, res))
        for i in range(3):
            res[i] = res[i][length[i] - num : length[i]]
            res[i] = list(map(lambda ques: ques.toSimpleJson(), res[i]))
            res[i].reverse()
        return {
            'tops': res[0],
            'topsDaily': res[1],
            'topsWeekly': res[2]
        }

    def toSimpleJson(self):
        '''Return simply serialized data of this question
        '''
        return {
            'id': self.id,
            'question_text': self.question_text,
            'category': self.category,
            'topic': self.topic,
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
            'visit_count': self.visit_count,
            'visit_count_daily': self.visit_count_daily,
            'visit_count_weekly': self.visit_count_weekly,
            'source': self.source,
            'entry_date': self.entry_date.timestamp() * 1e3
        }

    def validate(self, usersAnswer):
        '''Validate the answer provided by a user
        '''
        self.countInc()
        self.save()

    def countInc(self, *args, **kwargs):
        self.visit_count = F('visit_count') + 1
        self.visit_count_daily = F('visit_count_daily') + 1
        self.visit_count_weekly = F('visit_count_weekly') + 1

    def countResetDaily(self):
        self.visit_count_daily = 0

    def countResetWeekly(self):
        self.visit_count_daily = 0
        self.visit_count_weekly = 0

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