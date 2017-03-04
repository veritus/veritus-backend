import logging
import traceback
from django_cron import CronJobBase, Schedule
import case_gather.services as case_gathering_services
from parliament.models import ParliamentSession
from parliament.models import Parliament

cron_logger = logging.getLogger('cronJobs')


class gather_cases(CronJobBase):
    RUN_EVERY_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'case_gather.gather_cases'    # a unique code

    def do(self):
        session_number = 146
        try:
            PS_exists = ParliamentSession.objects.exists(
                session_number=session_number)
            assert PS_exists is False
            cron_logger.info('CREATING PARLIAMENT SESSION')
            Parliament.objects.create(name="current",
                                      start_date="2016-08-01",
                                      end_date="2020-08-01")

            parliament = Parliament.objects.get(name="current")
            ParliamentSession.objects.create(session_number=session_number,
                                             parliament=parliament)
        except Exception as e:
            cron_logger.error(e)
            
        try:
            cron_logger.info('Starting case gathering')

            case_gathering_services.update_case_db(session_number)
            cron_logger.info('Case gathering completed')
        except Exception as e:
            cron_logger.error(e.message + " - " + traceback.format_exc())
