from question.cron import trigger

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        trigger()