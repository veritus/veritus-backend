import traceback
import os

import case_gather.services as CaseGatheringService
from django_cron import CronJobBase, Schedule
import parliament.services as ParliamentServices
import main.sentryLogger as SentryLogger


class GatherCases(CronJobBase):
    RUN_EVERY_MINS = int(os.environ["GATHER_CASES_CRON_TIME_SECONDS"])

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.GatherCases'    # a unique code

    def do(self):
        try:
            SentryLogger.warning('Starting case gather')
            parliament_sessions = ParliamentServices.get_parliament_sessions_to_look_at()
            for parliament_session in parliament_sessions:
                print(parliament_session.session_number)
                CaseGatheringService.update_cases_by_session_number(
                    parliament_session)
            SentryLogger.warning('Case gather done')
        except BaseException:
            SentryLogger.error(traceback.format_exc())
            raise
