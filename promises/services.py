import logging

from promises.models import Promise, PromiseBill, SuggestedPromiseBill
from bill_gather.models import Bill, Parliament, ParliamentSession
from tags.models import Tag, BillTags, PromiseTags

cron_logger = logging.getLogger('cronJobs')

def find_connected_bills_and_promises():
    current_parliament = Parliament.objects.all().order_by('-id')[0]
    parliament_sessions = ParliamentSession.objects.filter(parliament=current_parliament)
    parliament_session_ids = []
    for parliament_session in parliament_sessions:
        parliament_session_ids.append(parliament_session.id)
    current_promises = Promise.objects.filter(parliament_session_id__in=parliament_session_ids)

    for parliament_session in parliament_sessions:
        session_bills = Bill.objects.filter(session=parliament_session)
        for bill in session_bills:
            bill_tags = BillTags.objects.filter(bill = bill)
            bill_tag_ids = []
            for bill_tag in bill_tags:
                bill_tag_ids.append(bill_tag.tag.id)
            tags_associated_with_bill = Tag.objects.filter(pk__in=bill_tag_ids)
            for promise in current_promises:
                promise_tags = PromiseTags.objects.filter(promise = promise)
                promise_tags_ids = []
                for promise_tag in promise_tags:
                    promise_tags_ids.append(promise_tag.tag.id)

                if len(bill_tag_ids) != 0 and len(promise_tags_ids) != 0:
                    number_of_common_tags = 0
                    if len(bill_tag_ids) >= len(promise_tags_ids):
                        size_of_larger_tag_array = len(bill_tag_ids)
                    else:
                        size_of_larger_tag_array = len(promise_tags_ids)

                    for bill_tag_id in bill_tag_ids:
                        cron_logger.info('billtagid: '+str(bill_tag_id))
                        cron_logger.info('promisetagid: '+str(promise_tags_ids))
                        cron_logger.info(bill_tag_id in promise_tags_ids)
                        if bill_tag_id in promise_tags_ids:
                            number_of_common_tags += 1
                    cron_logger.info(number_of_common_tags)
                    cron_logger.info(size_of_larger_tag_array)
                    cron_logger.info( float(number_of_common_tags) / float(size_of_larger_tag_array))




