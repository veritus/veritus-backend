import traceback
import os

from django_cron import CronJobBase, Schedule
from parliament.models import ParliamentSession
import votes.services as VoteServices
import main.sentryLogger as SentryLogger

class GatherVotes(CronJobBase):
    RUN_EVERY_MINS = int(os.environ["GATHER_VOTES_CRON_TIME_SECONDS"])
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'votes.GatherVotes'    # a unique code

    def do(self):
        try:
            SentryLogger.warning('Starting votes gather')
            PARLIAMENT_SESSIONS_TO_LOOK_AT = int(os.environ["PARLIAMENT_SESSIONS_TO_LOOK_AT"])
            parliament_sessions = ParliamentSession.objects.all().order_by('-id')[:PARLIAMENT_SESSIONS_TO_LOOK_AT]
            for parliament_session in parliament_sessions:
                VoteServices.get_votes_by_parliament_session(parliament_session)
            SentryLogger.warning('Votes gather done')
        except BaseException:
            SentryLogger.error(traceback.format_exc())
            raise
