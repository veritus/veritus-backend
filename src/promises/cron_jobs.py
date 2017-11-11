''' Cronjobs for promises '''
import traceback
import os
from django_cron import CronJobBase, Schedule
import promises.services as promise_services

import main.sentryLogger as SentryLogger

class ConnectBillsAndPromises(CronJobBase):
    ''' Connects bills and promises together using subjects that are related to both '''
    RUN_EVERY_MINS = int(os.environ["LINK_CASES_AND_PROMISES_CRON_TIME_SECONDS"])

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'promises.cron_jobs.connect_cases_and_promises'


    def do(self):
        ''' Executes the cron job '''
        try:
            SentryLogger.warning('Starting bill and promise connection')
            promise_services.find_connected_bills_and_promises()
            SentryLogger.warning('Completed bill and promise connection')

        except BaseException:
            SentryLogger.error(traceback.format_exc())
            raise
