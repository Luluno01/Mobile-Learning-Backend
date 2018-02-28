import sys
from time import sleep
from .models import OneChoiceQuestion
from .models import FillInQuestion
from .models import SubjectiveQuestion
from .models import TrueOrFalseQuestion
from .models import MultipleChoiceQuestion
import logging
logger = logging.getLogger("django")

QUESTIONS = [
    OneChoiceQuestion,
    MultipleChoiceQuestion,
    TrueOrFalseQuestion,
    FillInQuestion,
    SubjectiveQuestion
]

def countResetDaily():
    logger.warning('Resetting daily statistics...')
    for QuestionClass in QUESTIONS:
        for ques in QuestionClass.objects.all():
            ques.countResetDaily()
            ques.save()

def countResetWeekly():
    logger.warning('Resetting weekly statistics...')
    for QuestionClass in QUESTIONS:
        for ques in QuestionClass.objects.all():
            ques.countResetWeekly()
            ques.save()

def quit(signum, frame):
    sys.exit()

def trigger():
    import signal
    from threading import Timer
    from datetime import datetime, timedelta
    logger.info('Cron loaded')

    # Start cron

    def wrapper(func, everyFunc):
        def _wrapper():
            from .models import Cron
            cron = Cron.objects.all()
            if not cron:
                cron = Cron(last_run=datetime(year=1970, month=1, day=1))
            else:
                cron = cron[0]
            now = datetime.now()
            if cron.last_run.date == now.date:  # Already ran
                return  # Stop cron in this process
            logger.info('Last run time of cron job: %s' % cron.last_run)
            cron.last_run = datetime.now()
            cron.save()
            func()
            everyFunc()
        return _wrapper

    def everyDay():
        delta = timedelta(days=1)
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day
        weekday = today.weekday()
        today = datetime(year, month, day)
        nextDay = today + delta
        delta = nextDay - datetime.now()
        if weekday == 6:
            timer = Timer(delta.total_seconds(), wrapper(countResetWeekly, everyDay))
        else:
            timer = Timer(delta.total_seconds(), wrapper(countResetDaily, everyDay))
        timer.setDaemon(True)
        timer.start()
        logger.info('Next time to run cron job: %s' % nextDay)

    everyDay()
    sleepTime = 2 ** 22
    try:
        sleep(sleepTime)
    except OverflowError:
        sleepTime = 65535
    except KeyboardInterrupt:
        sys.exit()
    try:
        while True:
            sleep(sleepTime)
    except KeyboardInterrupt:
        pass

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)