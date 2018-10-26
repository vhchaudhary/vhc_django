from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task
from datetime import datetime
import random

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def cron_test():
    logger.info("Start task")
    now = datetime.now()
    logger.info("Task finished: result = %s" % now)


@shared_task
def shared_task_test(total):

    for i in range(total):
        logger.info("Shared Task: Random No = %s : %s" % (str(random.randint(1,1000)), str(i)))
