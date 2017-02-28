import logging

from promises.models import Promise, PromiseCase, SuggestedPromiseCase
from case_gather.models import Case
from parliament.models import Parliament, ParliamentSession
from tags.models import Tag, CaseTags, PromiseTags

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
        # We look at all bills in each parliament session within the current parliament
        for bill in session_bills:
            cron_logger.info('Bill Name: '+bill.name)
            bill_tags = BillTags.objects.filter(bill = bill)
            bill_tag_ids = []
            for bill_tag in bill_tags:
                # We take the bill tag ids to use later to compare to each promise tag id
                bill_tag_ids.append(bill_tag.tag.id)

            # We look at each promise within the same parliament session
            for promise in current_promises:
                cron_logger.info('Promise Name: '+promise.name)
                promise_tags = PromiseTags.objects.filter(promise = promise)
                promise_tags_ids = []
                for promise_tag in promise_tags:
                    # We take the promise tag ids to use later to compare to each bill tag id
                    promise_tags_ids.append(promise_tag.tag.id)

                if len(bill_tag_ids) != 0 and len(promise_tags_ids) != 0:
                    # We make sure the bill and the promise have tags
                    number_of_common_tags = 0
                    # We determine the larger array
                    if len(bill_tag_ids) >= len(promise_tags_ids):
                        size_of_larger_tag_array = len(bill_tag_ids)
                    else:
                        size_of_larger_tag_array = len(promise_tags_ids)

                    # We go through the bill tag ids and find any common tags in the promise tag id array
                    for bill_tag_id in bill_tag_ids:
                        cron_logger.info('billtagid: '+str(bill_tag_id))
                        cron_logger.info('promisetagid: '+str(promise_tags_ids))
                        cron_logger.info(bill_tag_id in promise_tags_ids)
                        if bill_tag_id in promise_tags_ids:
                            number_of_common_tags += 1

                    cron_logger.info(number_of_common_tags)
                    cron_logger.info(size_of_larger_tag_array)

                    # If the percent between common tags and the largest array reaches a certain point we want to
                    # connect the bill and promise. If
                    percent_of_common_tags = float(number_of_common_tags) / float(size_of_larger_tag_array)
                    cron_logger.info( percent_of_common_tags)
                    # We want at least 4 tags on both the bill and the promise
                    if len(bill_tag_ids) > 4 and len(promise_tags_ids) > 4:
                        cron_logger.info('Bill and promise have more than 4 tags each')
                        # If the percent is 80% or higher we make a connection
                        if percent_of_common_tags >= 0.8:
                            PromiseBill.objects.create(bill=bill, promise=promise)
                            cron_logger.info('PromiseBill connection created')
                        # If the percent is between 50% and 79% we create a suggested connection
                        elif percent_of_common_tags >= 0.5:
                            SuggestedPromiseBill.objects.create(bill=bill, promise=promise)
                            cron_logger.info('SuggestedPromiseBill connection created')







