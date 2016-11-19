import requests, datetime, logging
from bs4 import BeautifulSoup
from bill_gather.models import ParliamentSession, Bill

cron_logger = logging.getLogger('cronJobs')

def scrape_by_parliament_session_number(parliament_session_number):
    result = requests.get("http://www.althingi.is/thingstorf/thingmalalistar-eftir-thingum/lagafrumvorp/?lthing="+str(parliament_session_number))
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    bill_table = soup.find_all("table", id="t_malalisti")[0]
    bill_table_body = bill_table.find_all("tbody")[0]
    bill_rows = bill_table_body.find_all("tr")

    parliament_session = ParliamentSession.objects.get(session_number=parliament_session_number)

    current_parliament_session_bills = Bill.objects.filter(session=parliament_session)
    # We use this list to determine whether to create a new bill or if it exists already
    bill_number_list = []
    for bill in current_parliament_session_bills:
        bill_number_list.append(bill.number)


    for bill_row in bill_rows:
        columns = bill_row.find_all('td')
        bill_number = int(columns[0].getText())
        bill_date = columns[1].getText().split('.')
        bill_name = columns[2].getText()
        if bill_number not in bill_number_list:
            cron_logger.info('Created: '+ columns[0].getText())
            Bill.objects.create(number=bill_number,
                                name=bill_name,
                                session=parliament_session,
                                description='',
                                created_date=datetime.date(int(bill_date[2]), int(bill_date[1]), int(bill_date[0])))