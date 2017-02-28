import logging
import traceback
from django_cron import CronJobBase, Schedule
import case_gather.services as case_gathering_services

cron_logger = logging.getLogger('cronJobs')


class gather_cases(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.gather_cases'    # a unique code

    def do(self):
        try:
            cron_logger.info('Starting case gathering')
            session_number = 146
            case_gathering_services.update_case_db(session_number)
            cron_logger.info('Case gathering completed')
        except Exception as e:
            cron_logger.error(e.message + " - " + traceback.format_exc())
