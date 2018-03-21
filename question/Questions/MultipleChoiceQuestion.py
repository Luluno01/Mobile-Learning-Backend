import json
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q, F
from django.db import models
from django.utils import timezone
from .ChoiceQuestion import ChoiceQuestion, Choice
import logging
logger = logging.getLogger("django")

def __defaultList__():
    return []

class MultipleChoiceQuestion(ChoiceQuestion):
    '''Multiple-choice question
    '''
    answer = ArrayField(models.IntegerField(default=0), default=__defaultList__)  # Answers of this question
    correct_count = models.IntegerField(default=0)

    CHOICE_CLASS = None

    @classmethod
    def create(cls, *args, **kwargs):
        '''Create an MultipleChoiceQuestion object

        Create an MultipleChoiceQuestion object and save if choices are provided
        '''
        if 'json' in kwargs:
            obj = {}
            if type(kwargs['json']) == str:
                obj = json.loads(kwargs['json'])
            elif type(kwargs['json'] == dict):
                obj = kwargs['json']
            else:
                raise TypeError('Unsupported type of key word `json`')
            del kwargs['json']
            
            # Data checks
            if type(obj['answer']) != list:
                raise ValueError('Invalid type of `answer`')
            # if len(obj['answer']) == 1:
            #     raise ValueError('Length of choices of a multiple-choice question should be more than 1')

            choiceLength = len(obj['choices'])
            obj['answer'] = list(set(obj['answer']))  # Removed duplicated answers
            for ans in obj['answer']:
                if ans < 0 or ans >= choiceLength:
                    raise ValueError('Invalid answer index')

            # Create choice set
            choices = []
            for choiceIndex, choice in enumerate(obj['choices']):
                choices.append(OneChoiceChoice(**choice))
                choices[choiceIndex].save()
            del obj['choices']

            # Create question
            obj['answer'] = list(map(lambda ans: choices[ans].id, obj['answer']))
            question = cls(*args, **obj)
            question.entry_date = timezone.now()
            question.save()
            for choice in choices:
                choice.question = question
                choice.save()
        else:
            question = cls(*args, **kwargs)
            question.entry_date = timezone.now()

        return question

    def countInc(self, correct=False, *args, **kwargs):
        self.visit_count = F('visit_count') + 1
        self.visit_count_daily = F('visit_count_daily') + 1
        self.visit_count_weekly = F('visit_count_weekly') + 1
        if correct:
            self.correct_count = F('correct_count') + 1
            self.correct_count_daily = F('correct_count_daily') + 1
            self.correct_count_weekly = F('correct_count_weekly') + 1

    def validate(self, usersAnswer):
        '''Validate the answer provided by a user
        '''
        if type(usersAnswer) != list or not usersAnswer or type(usersAnswer[0]) != int:
            raise ValueError('Invalid type of answer')

        usersAnswer = list(set(usersAnswer))

        condition = Q(pk=self.answer[0])
        for answerIndex, answer in enumerate(self.answer):
            if answerIndex == 0:
                continue
            condition |= Q(pk=answer)
        answers = MultipleChoiceChoice.objects.filter(condition)
        if not answers:
            logger.error('Broken question %s' % self)
            return
        correct = False
        if set(usersAnswer) == set(self.answer):  # Correct
            self.accuracy = (self.correct_count + 1) / (self.visit_count + 1)
            correct = True
            for ans in answers:
                ans.countInc()
                ans.save()
        elif set(usersAnswer) == set([0]):  # The user does not choose an answer
            self.accuracy = self.correct_count / (self.visit_count + 1)
        else:  # Wrong
            condition = Q(pk=usersAnswer[0])
            for answerIndex, answer in enumerate(usersAnswer):
                if answerIndex == 0:
                    continue
                condition |= Q(pk=answer)
            _usersAnswer = MultipleChoiceChoice.objects.filter(condition, question=self)
            if len(_usersAnswer) != len(usersAnswer):
                logger.info('Unmatched answers %s' % usersAnswer)
                raise ValueError('Unmatched answers %s' % usersAnswer)
            self.accuracy = self.correct_count / (self.visit_count + 1)
            for ans in _usersAnswer:
                ans.countInc()
                ans.save()
        self.countInc(correct)
        self.save()

    def answer_number_and_id(self):
        choices = MultipleChoiceChoice.objects.filter(question=self)
        if not choices:
            logger.warning('No choices for question %s' % self)
            return 'No answer'
        # logger.debug('%s' % [choice.id for choice in choices])
        res = []
        for choiceIndex, choice in enumerate(choices):
            if choice.id in self.answer:
                res.append('%s/%s' % (choiceIndex + 1, choice.id))
        return ', '.join(res)
    answer_number_and_id.empty_value_display = 'No answer'

    @classmethod
    def clearNoAnswer(cls):
        '''Clear questions with invalid answer
        '''
        logger.warning('Clearing questions with invalid answer')
        return cls.objects.filter(Q(answer=[]) | Q(answer=None)).delete()

    @classmethod
    def clearNoChoice(cls):
        '''Scan and clear bad questions

        Scan and clear bad questions which has no choices or has invalid answer

        Returns:

            `deleted`: {list} A list of deleted questions.

            `broken`: {list} A list of broken questions that some of whose answers belong to other questions.

            `wild`: {list} A list of questions that have unmatched answers.
        '''
        logger.warning('Clearing questions with no choices')
        deleted = []
        broken = []
        wild = []
        for question in cls.objects.all():
            choices = MultipleChoiceChoice.objects.filter(question=question)
            if not choices:  # Question with no choices found
                logger.info('Question with no choices found (id: %d), deleting...' % question.id)
                deleted.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'answer': question.answer,
                    'resolution': question.resolution,
                    'category': question.category,
                    'topic': question.topic,
                    'visit_count': question.visit_count,
                    # 'accuracy': question.accuracy,
                    'source': question.source,
                    'entry_date': question.entry_date.timestamp() * 1e3
                    # 'reason': xxx
                })
                question.delete()
                continue
            condition = Q(pk=question.answer[0])
            for answerIndex, answer in enumerate(question.answer):
                if answerIndex == 0:
                    continue
                condition |= Q(pk=answer)
            answers = MultipleChoiceChoice.objects.filter(condition)
            if not answers:  # Bad answer found
                logger.info('Question with invalid answers found (id: %d), deleting...' % question.id)
                deleted.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'answer': question.answer,
                    'resolution': question.resolution,
                    'category': question.category,
                    'topic': question.topic,
                    'visit_count': question.visit_count,
                    # 'accuracy': question.accuracy,
                    'source': question.source,
                    'entry_date': question.entry_date.timestamp() * 1e3
                    # 'reason': xxx
                })
                question.delete()
                continue
            wildAnswerCount = 0
            for answer in answers:
                if answer.question.id != question.id:
                    wildAnswerCount += 1
            if 0 < wildAnswerCount and wildAnswerCount < len(answers):  # Broken answer found
                logger.warning('Broken question with some of its answers belong to other questions found (id: %d), reserved' % question.id)
                broken.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'answer': question.answer,
                    'resolution': question.resolution,
                    'category': question.category,
                    'topic': question.topic,
                    'visit_count': question.visit_count,
                    # 'accuracy': question.accuracy,
                    'source': question.source,
                    'entry_date': question.entry_date.timestamp() * 1e3
                    # 'reason': xxx
                })
                continue
                # question.delete()
            if wildAnswerCount == len(answers):  # Wild answer found
                logger.info('Wild question with all its answers belong to other questions found (id: %d), reserved' % question.id)
                wild.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'answer': question.answer,
                    'resolution': question.resolution,
                    'category': question.category,
                    'topic': question.topic,
                    'visit_count': question.visit_count,
                    # 'accuracy': question.accuracy,
                    'source': question.source,
                    'entry_date': question.entry_date.timestamp() * 1e3
                    # 'reason': xxx
                })
        return deleted, broken, wild

class MultipleChoiceChoice(Choice):
    '''Choice of a multiple-choice question
    '''
    question = models.ForeignKey(MultipleChoiceQuestion, models.CASCADE, null=True)
    pass

MultipleChoiceQuestion.CHOICE_CLASS = MultipleChoiceChoice