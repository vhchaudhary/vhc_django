from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime


def my_scheduled_job():
    print(datetime.datetime.now(), " -- ***** cron job has started ***** \n")
