import requests, datetime, logging
from bs4 import BeautifulSoup
from bill_gather.models import ParliamentSession, Bill, Tag, BillTags

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
        bill_name_column = columns[2]
        bill_name = bill_name_column.getText()
        bill_name_link = bill_name_column.find('a')['href']

        # We only want to add bills that are not in the database
        if bill_number not in bill_number_list:
            cron_logger.info('Creating: '+ columns[0].getText())

            bill_process_page = requests.get('http://www.althingi.is'+bill_name_link)
            bill_process_content = bill_process_page.content
            bill_process_soup = BeautifulSoup(bill_process_content, 'html.parser')

            # Search for document description
            document_link = find_document_description_link(bill_process_soup)

            # Identify and save tags for bill


            bill = Bill.objects.create(number=bill_number,
                               name=bill_name,
                               session=parliament_session,
                                description_link='http://www.althingi.is'+document_link,
                                created_date=datetime.date(int(bill_date[2]), int(bill_date[1]), int(bill_date[0])))

            identify_and_save_tags(bill_process_soup, bill)


def identify_and_save_tags(bill_process_soup, bill):
    ul = bill_process_soup.find('ul')

    tag_link = ul.find_all('li')[0].find('a')['href']
    cron_logger.info(tag_link)
    bill_tag_page = requests.get('http://www.althingi.is'+tag_link)
    bill_tag_content = bill_tag_page.content
    bill_tag_soup = BeautifulSoup(bill_tag_content, 'html.parser')
    cron_logger.info(bill_tag_soup.find_all('div', {'class': 'article box news'})[0].find_all('ul')[1].find_all('li'))
    tag_list = bill_tag_soup.find_all('div', {'class': 'article box news'})[0].find_all('ul')[1].find_all('li')

    cron_logger.info(tag_list)
    for tag in tag_list:
        tag_name = tag.getText()
        if Tag.objects.filter(name = tag_name).count() == 0:
            # Tag doesnt exist, we create it and tie to bill
            tag = Tag.objects.create(name=tag_name)
            BillTags.objects.create(bill=bill, tag=tag)
        else:
            BillTags.objects.create(bill=bill, tag=Tag.objects.get(name = tag_name))

def find_document_description_link(bill_process_soup):
    document_table = bill_process_soup.find('table')
    cron_logger.info(document_table)
    parliament_document_rows = document_table.find_all('tr')
    document_link = ''

    for row in parliament_document_rows:
        cron_logger.info(row)
        columns = row.find_all('td')
        if len(columns) != 0:
            document_date = columns[0].getText().split('.')
            document_link_column =  columns[1]
            document_link = document_link_column.find('a')['href']
            cron_logger.info('http://www.althingi.is'+document_link)
    return document_link