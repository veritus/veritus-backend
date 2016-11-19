import logging, traceback, requests
from django_cron import CronJobBase, Schedule
from bs4 import BeautifulSoup
from bill_gather.models import ParliamentSession, Bill

cron_logger = logging.getLogger('cronJobs')


class gather_bills(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bill_gather.gather_bills'    # a unique code


    def do(self):
        # TODO:
        # If embargoed - Zenodo might require an embargo date (might be better to just close it if embargoed?)
        try:
            cron_logger.info('Starting bill gather')
            session_number = 145
            result = requests.get("http://www.althingi.is/thingstorf/thingmalalistar-eftir-thingum/lagafrumvorp/?lthing="+str(session_number))
            c = result.content
            soup = BeautifulSoup(c, 'html.parser')
            bill_table = soup.find_all("table", id="t_malalisti")[0]
            bill_table_body = bill_table.find_all("tbody")[0]
            bill_rows = bill_table_body.find_all("tr")
            cron_logger.info(bill_rows)

            parliament_session = ParliamentSession.objects.get(session_number=session_number)

            current_parliament_session_bills = Bill.objects.filter(session=parliament_session)
            bill_number_list = []
            for bill in current_parliament_session_bills:
                bill_number_list.append(bill.number)


            for bill_row in bill_rows:
                columns = bill_row.find_all('td')
                bill_number = int(columns[0].getText())
                bill_date = columns[1].getText()
                bill_name = columns[2].getText()
                if bill_number not in bill_number_list:
                    cron_logger.info('Created: '+ columns[0].getText())
                    Bill.objects.create(number=bill_number, name=bill_name, session=parliament_session, description='')








        except Exception as e:
            cron_logger.error(e.message + " - " + traceback.format_exc())
