''' Cronjobs for promises '''
import logging
import traceback
from django_cron import CronJobBase, Schedule
import promises.services as promise_services

CRONLOGGER = logging.getLogger('cronJobs')

class ConnectBillsAndPromises(CronJobBase):
    ''' Connects bills and promises together using subjects that are related to both '''
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'promises.cron_jobs.connect_cases_and_promises'


    def do(self):
        ''' Executes the cron job '''
        try:
            CRONLOGGER.info('Starting bill and promise connection')
            promise_services.find_connected_bills_and_promises()
            CRONLOGGER.info('Completed bill and promise connection')

        except BaseException:
            CRONLOGGER.error(traceback.format_exc())
            raise