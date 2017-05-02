import logging

from promises.models import Promise, PromiseCase, SuggestedPromiseCase
from case_gather.models import Case
from parliament.models import Parliament, ParliamentSession
from subjects.models import CaseSubject, PromiseSubject

cron_logger = logging.getLogger('cronJobs')


def find_connected_bills_and_promises():
    current_parliament = Parliament.objects.all().order_by('-id')[0]
    parliament_sessions = ParliamentSession.objects.filter(parliament=current_parliament)
    parliament_session_ids = []
    for parliament_session in parliament_sessions:
        parliament_session_ids.append(parliament_session.id)
    current_promises = Promise.objects.filter(parliament_session_id__in=parliament_session_ids)

    for parliament_session in parliament_sessions:
        session_cases = Case.objects.filter(session=parliament_session)
        # We look at all bills in each parliament session within the current parliament
        for case in session_bills:
            cron_logger.info('Case Name: '+case.name)
            case_subjecs = CaseSubject.objects.filter(case = case)
            case_subect_ids = []
            for case_subject in case_subjects:
                # We take the bill subject ids to use later to compare to each promise subject id
                case_subject_ids.append(case_subject.subject.id)

            # We look at each promise within the same parliament session
            for promise in current_promises:
                cron_logger.info('Promise Name: '+promise.name)
                promise_subjects = PromiseSubject.objects.filter(promise = promise)
                promise_subject_ids = []
                for promise_subject in promise_subjects:
                    # We take the promise suject ids to use later to compare to each bill subject id
                    promise_subjects_ids.append(promise_subject.subject.id)

                if len(bill_subject_ids) != 0 and len(promise_subjects_ids) != 0:
                    # We make sure the bill and the promise have subjects
                    number_of_common_subjects = 0
                    # We determine the larger array
                    if len(bill_subject_ids) >= len(promise_subjects_ids):
                        size_of_larger_subject_array = len(bill_subject_ids)
                    else:
                        size_of_larger_subject_array = len(promise_subjects_ids)

                    # We go through the bill subject ids and find any common subjects in the promise subject id array
                    for bill_subject_id in bill_subject_ids:
                        cron_logger.info('bill subject id: '+str(bill_subject_id))
                        cron_logger.info('promise subject id: '+str(promise_subjects_ids))
                        cron_logger.info(bill_subject_id in promise_subjects_ids)
                        if bill_subject_id in promise_subjects_ids:
                            number_of_common_subjects += 1

                    cron_logger.info(number_of_common_subjects)
                    cron_logger.info(size_of_larger_subject_array)

                    # If the percent between common subjects and the largest array reaches a certain point we want to
                    # connect the bill and promise. If
                    percent_of_common_subjects = float(number_of_common_subjects) / float(size_of_larger_subject_array)
                    cron_logger.info( percent_of_common_subjects)
                    # We want at least 4 subjects on both the bill and the promise
                    if len(bill_subject_ids) > 4 and len(promise_subjects_ids) > 4:
                        cron_logger.info('Bill and promise have more than 4 subjects each')
                        # If the percent is 80% or higher we make a connection
                        if percent_of_common_subjects >= 0.8:
                            PromiseBill.objects.create(bill=bill, promise=promise)
                            cron_logger.info('PromiseBill connection created')
                        # If the percent is between 50% and 79% we create a suggested connection
                        elif percent_of_common_subjects >= 0.5:
                            SuggestedPromiseBill.objects.create(bill=bill, promise=promise)
                            cron_logger.info('SuggestedPromiseBill connection created')







