import logging
import traceback
import os

import services as CaseGatheringService
from django_cron import CronJobBase, Schedule
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

            CaseGatheringService.update_cases_by_session_number(session_number)
            CRONLOGGER.info('Case gathering completed')
        except BaseException:
            CRONLOGGER.error(traceback.format_exc())
            raise
