from django.db.models.signals import post_save
from django.apps import AppConfig


def updateList(sender, **kwargs):
    from .models import QuestionList
    import logging
    logger = logging.getLogger("django")

    questionList = QuestionList.objects.all()
    if not questionList:
        questionList = QuestionList()
    else:
        questionList = questionList[0]
    questionList.update()
    questionList.save()

class QuestionConfig(AppConfig):
    name = 'question'

    def ready(self, *args, **kwargs):
        # Register signal
        # This stupid signal doesn't work at all
        post_save.connect(updateList, sender=self, weak=False)