import traceback
import os

from django_cron import CronJobBase, Schedule
import parliament.services as ParliamentServices
import votes.services as VoteServices
import main.sentryLogger as SentryLogger


class GatherVotes(CronJobBase):
    RUN_EVERY_MINS = int(os.environ["GATHER_VOTES_CRON_TIME_SECONDS"])

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'votes.GatherVotes'    # a unique code

    def do(self):
        try:
            SentryLogger.warning('Starting votes gather')
            parliament_sessions = ParliamentServices.get_parliament_sessions_to_look_at()
            for parliament_session in parliament_sessions:
                VoteServices.get_votes_by_parliament_session(
                    parliament_session)
            SentryLogger.warning('Votes gather done')
        except BaseException:
            SentryLogger.error(traceback.format_exc())
            raise
