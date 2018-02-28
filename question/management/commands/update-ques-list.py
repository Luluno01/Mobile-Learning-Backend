from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from question.models import QuestionList
        import logging
        logger = logging.getLogger("django")

        questionList = QuestionList.objects.all()
        if not questionList:
            questionList = QuestionList()
        else:
            questionList = questionList[0]
        questionList.update()
        questionList.save()