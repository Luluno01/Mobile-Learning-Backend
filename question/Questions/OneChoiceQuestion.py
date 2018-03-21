import json
from django.db import models
from django.utils import timezone
from .ChoiceQuestion import ChoiceQuestion, Choice
import logging
logger = logging.getLogger("django")

class OneChoiceQuestion(ChoiceQuestion):
    '''One-choice question
    '''
    answer = models.IntegerField(default=0)  # Answer of this question
    
    CHOICE_CLASS = None

    @staticmethod
    def newOneChoiceQuestion(*args, **kwargs):
        question = __class__(*args, **kwargs)
        return question

    @classmethod
    def create(cls, *args, **kwargs):
        '''Create an OneChoiceQuestion object

        Create an OneChoiceQuestion object and save if choices are provided
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
            if obj['answer'] < 0 or obj['answer'] >= len(obj['choices']):
                raise ValueError('Invalid answer index')

            # Create choice set
            choices = []
            for choiceIndex, choice in enumerate(obj['choices']):
                choices.append(OneChoiceChoice(**choice))
                choices[choiceIndex].save()
            del obj['choices']

            # Create question
            answerIndex = obj['answer']
            obj['answer'] = choices[answerIndex].id
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

    def validate(self, usersAnswer):
        '''Validate the answer provided by a user
        '''
        try:
            answer = OneChoiceChoice.objects.get(pk=self.answer)
        except OneChoiceChoice.DoesNotExist:
            logger.error('Broken question %s' % self)
            return
        correct = False
        if usersAnswer == self.answer:  # Correct
            self.accuracy = (answer.selection_count + 1) / (self.visit_count + 1)
            answer.countInc()
            answer.save()
            correct = True
        elif usersAnswer == 0:  # The user does not choose an answer
            self.accuracy = answer.selection_count / (self.visit_count + 1)
        else:  # Wrong
            try:
                _usersAnswer = OneChoiceChoice.objects.get(pk=usersAnswer, question=self)
                self.accuracy = answer.selection_count / (self.visit_count + 1)
                _usersAnswer.countInc()
                _usersAnswer.save()
            except OneChoiceChoice.DoesNotExist:
                logger.info('No such answer with id %d' % usersAnswer)
                raise ValueError('No such answer with id %d' % usersAnswer)
        self.countInc(correct)
        self.save()

    def answer_number_and_id(self):
        choices = OneChoiceChoice.objects.filter(question=self)
        if not choices:
            logger.warning('No choices for question %s' % self)
            return 'No answer'
        # logger.debug('%s' % [choice.id for choice in choices])
        for choiceIndex, choice in enumerate(choices):
            if choice.id == self.answer:
                return '%s/%s' % (choiceIndex + 1, self.answer)
        return 'No answer'

    @classmethod
    def clearNoAnswer(cls):
        '''Clear questions with invalid answer
        '''
        logger.warning('Clearing questions with invalid answer')
        return cls.objects.filter(answer=0).delete()

    @classmethod
    def clearNoChoice(cls):
        '''Scan and clear bad questions

        Scan and clear bad questions which has no choices or has invalid answer

        Returns:

            `deleted`: {list} A list of deleted questions.

            `wild`: {list} A list of questions that have unmatched answers.
        '''
        logger.warning('Clearing questions with no choices')
        deleted = []
        wild = []
        for question in cls.objects.all():
            choices = OneChoiceChoice.objects.filter(question=question)
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
            try:
                answer = OneChoiceChoice.objects.get(pk=question.answer)
                if not answer.question or answer.question.id != question.id:
                    logger.warning('Question with answer that belongs to another question found (id: %d), reserved' % question.id)
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
                    # question.delete()
            except OneChoiceChoice.DoesNotExist:  # Bad answer found
                logger.info('Question with invalid answer found (id: %d), deleting...' % question.id)
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
        return deleted, wild

class OneChoiceChoice(Choice):
    '''Choice of a one-choice question
    '''
    question = models.ForeignKey(OneChoiceQuestion, models.CASCADE, null=True)
    pass

OneChoiceQuestion.CHOICE_CLASS = OneChoiceChoice