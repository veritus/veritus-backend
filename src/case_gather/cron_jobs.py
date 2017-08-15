import logging
import traceback
import os
from django_cron import CronJobBase, Schedule
import case_gather.services as case_gathering_services
from parliament.models import ParliamentSession

CRONLOGGER = logging.getLogger('cronJobs')

class GatherCases(CronJobBase):
    RUN_EVERY_MINS = os.environ["GATHER_CASES_CRON_TIME_SECONDS"]

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.GatherCases'    # a unique code

    def do(self):
        try:
            CRONLOGGER.info('Starting case gathering')
            session_number = ParliamentSession.objects.latest('created').session_number

            case_gathering_services.update_case_db(session_number)
            CRONLOGGER.info('Case gathering completed')
        except Exception as exception:
            CRONLOGGER.error(traceback.format_exc())
            raise
