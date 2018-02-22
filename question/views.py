from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import OneChoiceQuestion, OneChoiceChoice
import logging
logger = logging.getLogger("django")

# Create your views here.

class OneChoiceQuestionView():
    @staticmethod
    def getSimpleList(request, *args, **kwargs):
        if kwargs['category']:
            try:
                kwargs['category'] = int(kwargs['category'])
                _allQues = list(OneChoiceQuestion.objects.filter(category=kwargs['category']))
            except ValueError:
                _allQues = list(OneChoiceQuestion.objects.all())
        else:
            _allQues = list(OneChoiceQuestion.objects.all())
        allQues = list(map(lambda ques: ques.toSimpleJson(), _allQues))
        return JsonResponse(allQues, safe=False)

    @staticmethod
    def getSimpleQuestionInfo(request, *args, **kwargs):
        question = get_object_or_404(OneChoiceQuestion, pk=kwargs['question'])
        return JsonResponse(question.toSimpleJson(), safe=False)

    @staticmethod
    def getFullQuestionInfo(request, *args, **kwargs):
        question = get_object_or_404(OneChoiceQuestion, pk=kwargs['question'])
        return JsonResponse(question.toJson(), safe=False)

    @staticmethod
    def validate(request, *args, **kwargs):
        try:
            question_id = int(kwargs['question'])
            answer_id = int(kwargs['answer'])
            question = get_object_or_404(OneChoiceQuestion, pk=question_id)
            question.validate(answer_id)
            return HttpResponse('OK')
        except ValueError as e:
            logger.debug(e)
            return HttpResponseBadRequest('Validate failed')