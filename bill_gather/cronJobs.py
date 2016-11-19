import logging, traceback
from django_cron import CronJobBase, Schedule
import services as bill_gathering_services

cron_logger = logging.getLogger('cronJobs')


class gather_bills(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bill_gather.gather_bills'    # a unique code


    def do(self):
        # TODO:
        # If embargoed - Zenodo might require an embargo date (might be better to just close it if embargoed?)
        try:
            cron_logger.info('Starting bill gather')
            session_number = 145
            bill_gathering_services.scrape_by_parliament_session_number(session_number)








        except Exception as e:
            cron_logger.error(e.message + " - " + traceback.format_exc())
