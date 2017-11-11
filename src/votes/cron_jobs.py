import logging
import traceback
import os
import logging

from django_cron import CronJobBase, Schedule
from parliament.models import ParliamentSession
import votes.services as VoteServices

CRONLOGGER = logging.getLogger('cronJobs')

class GatherVotes(CronJobBase):
    RUN_EVERY_MINS = os.environ["GATHER_VOTES_CRON_TIME_SECONDS"]

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.GatherVotes'    # a unique code

    def do(self):
        try:
            CRONLOGGER.info('Starting votes gather')
            parliament_session = ParliamentSession.objects.latest('created')
            VoteServices.get_votes_by_parliament_session(parliament_session)
            CRONLOGGER.info('Votes gather done')
        except BaseException:
            CRONLOGGER.error(traceback.format_exc())
            raise
