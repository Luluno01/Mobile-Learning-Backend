from django.contrib.postgres.fields import JSONField
from django.db import models
from .Question import Question
from .OneChoiceQuestion import OneChoiceQuestion
from .MultipleChoiceQuestion import MultipleChoiceQuestion
from .TrueOrFalseQuestion import TrueOrFalseQuestion
from .FillInQuestion import FillInQuestion
from .SubjectiveQuestion import SubjectiveQuestion
import logging
logger = logging.getLogger("django")

def __defaultDict__():
    return {}

QUESTIONS = [
    OneChoiceQuestion,
    MultipleChoiceQuestion,
    TrueOrFalseQuestion,
    FillInQuestion,
    SubjectiveQuestion
]

class QuestionList(models.Model):
    one_choice_question = JSONField(default=__defaultDict__)
    multiple_choice_question = JSONField(default=__defaultDict__)
    true_or_false_question = JSONField(default=__defaultDict__)
    fill_in_question = JSONField(default=__defaultDict__)
    subjective_question = JSONField(default=__defaultDict__)

    map = {
        OneChoiceQuestion.__name__: 'one_choice_question',
        MultipleChoiceQuestion.__name__: 'multiple_choice_question',
        TrueOrFalseQuestion.__name__: 'true_or_false_question',
        FillInQuestion.__name__: 'fill_in_question',
        SubjectiveQuestion.__name__: 'subjective_question'
    }

    def getList(self, QuestionClass):
        return getattr(self, __class__.map[QuestionClass.__name__])

    def update(self, QeustionClasses=QUESTIONS):
        try:
            for QuestionClass in QeustionClasses:
                logger.info('Updating question id list for %s' % QuestionClass.__name__)
                questions = QuestionClass.objects.all()
                newList = []
                for category in Question.CATEGORY:
                    newList.append([])
                for ques in questions:
                    newList[ques.category - 1].append(ques.id)
                setattr(self, __class__.map[QuestionClass.__name__], newList)
        except KeyError:
            raise ValueError('Invalid class of question')