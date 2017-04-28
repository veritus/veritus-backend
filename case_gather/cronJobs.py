import logging
import traceback
from django_cron import CronJobBase, Schedule
import case_gather.services as case_gathering_services
from parliament.models import ParliamentSession
from parliament.models import Parliament

cron_logger = logging.getLogger('cronJobs')


class gather_cases(CronJobBase):
    RUN_EVERY_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.gather_cases'    # a unique code

    def do(self):
        session_number = 146
            
        try:
            cron_logger.info('Starting case gathering')

            case_gathering_services.update_case_db(session_number)
        except Exception as e:
            cron_logger.error(e.message + " - " + traceback.format_exc())
        finally:
            cron_logger.info('Case gathering completed')

        try:
            cron_logger.info('Starting subject gathering')

            case_gathering_services.update_subject_db()

        except Exception as e:
            cron_logger.error(e.message + ' - ' + traceback.format_exc())
        finally:
            cron_logger.info('Subject gathering completed')