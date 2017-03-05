import logging
import traceback
from django_cron import CronJobBase, Schedule
import promises.services as promise_services

cron_logger = logging.getLogger('cronJobs')

# class connect_bills_and_promises(CronJobBase):
#     RUN_EVERY_MINS = 1

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'promise.connect_bills_and_promises'    # a unique code


#     def do(self):
#         try:
#             cron_logger.info('Starting bill and promise connection')
#             promise_services.find_connected_bills_and_promises()

#         except Exception as e:
#             cron_logger.error(e.message + " - " + traceback.format_exc())
