import json
from json.decoder import JSONDecodeError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .Questions.Question import Question
from .models import OneChoiceQuestion, OneChoiceChoice
from .models import FillInQuestion
from .models import SubjectiveQuestion
from .models import TrueOrFalseQuestion
from .models import MultipleChoiceQuestion, MultipleChoiceChoice
from .models import QuestionList
from Lib.RequestParamParser import RequestParamParser
import logging
logger = logging.getLogger("django")

# Create your views here.

class QuestionView():
    '''Base class for views for Question
    '''
    QuestionClass = Question
    validateAnswer = True

    @classmethod
    def getSimpleList(cls, request, *args, **kwargs):
        if kwargs['category']:
            try:
                kwargs['category'] = int(kwargs['category'])
                _allQues = list(cls.QuestionClass.objects.filter(category=kwargs['category']))
            except ValueError:
                _allQues = list(cls.QuestionClass.objects.all())
        else:
            _allQues = list(cls.QuestionClass.objects.all())
        allQues = list(map(lambda ques: ques.toSimpleJson(), _allQues))
        return JsonResponse(allQues, safe=False)

    @classmethod
    def getIdList(cls, request, *args, **kwargs):
        questionList = QuestionList.objects.all()
        if not questionList:
            questionList = QuestionList()
            questionList.update()
            questionList.save()
        else:
            questionList = questionList[0]

        if kwargs['category']:
            try:
                kwargs['category'] = int(kwargs['category'])
                _list = questionList.getList(cls.QuestionClass)[kwargs['category'] - 1]
            except ValueError:
                _list = questionList.getList(cls.QuestionClass)
            except IndexError:
                return HttpResponseBadRequest('Invalid category')
        else:
            _list = questionList.getList(cls.QuestionClass)
        return JsonResponse(_list, safe=False)

    @classmethod
    def getSimpleQuestionInfo(cls, request, *args, **kwargs):
        question = get_object_or_404(cls.QuestionClass, pk=kwargs['question'])
        return JsonResponse(question.toSimpleJson(), safe=False)

    @classmethod
    def getFullQuestionInfo(cls, request, *args, **kwargs):
        question = get_object_or_404(cls.QuestionClass, pk=kwargs['question'])
        return JsonResponse(question.toJson(), safe=False)

    @classmethod
    def validate(cls, request, *args, **kwargs):
        RequestParamParser(request, kwargs)

        if 'question' not in request.params or type(request.params['question']) != int:
            return HttpResponseBadRequest('Validate failed')

        answer = None
        if cls.validateAnswer:
            if 'answer' not in request.params:
                return HttpResponseBadRequest('Validate failed')
            answer = request.params['answer']

        question = get_object_or_404(cls.QuestionClass, pk=request.params['question'])
        try:
            question.validate(answer)
        except ValueError as e:
            logger.info(e)
            logger.info(request.params)
            return HttpResponseBadRequest('Validate failed')
        return HttpResponse('OK')

class OneChoiceQuestionView(QuestionView):
    QuestionClass = OneChoiceQuestion
    pass

class FillInQuestionView(QuestionView):
    QuestionClass = FillInQuestion
    validateAnswer = False

class SubjectiveQuestionView(QuestionView):
    QuestionClass = SubjectiveQuestion
    validateAnswer = False

class TrueOrFalseQuestionView(QuestionView):
    QuestionClass = TrueOrFalseQuestion
    validateAnswer = True

class MultipleChoiceQuestionView(QuestionView):
    QuestionClass = MultipleChoiceQuestion
    validateAnswer = True