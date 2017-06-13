import logging
import traceback
from django_cron import CronJobBase, Schedule
import case_gather.services as case_gathering_services

CRONLOGGER = logging.getLogger('cronJobs')

class GatherCases(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.GatherCases'    # a unique code

    def do(self):
        session_number = 146

        try:
            CRONLOGGER.info('Starting case gathering')
            case_gathering_services.update_case_db(session_number)
        except Exception as exception:
            CRONLOGGER.error(exception.message + " - " + traceback.format_exc())
        finally:
            CRONLOGGER.info('Case gathering completed')
