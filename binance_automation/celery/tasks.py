from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task
from config.settings.base import env

log = get_task_logger(__name__)

class TrackingLoadUtils():
    """..."""
    # @periodic_task(run_every=(crontab(minute=0, hour=0, day_of_month='15,30')), name='example')
    # def example():
