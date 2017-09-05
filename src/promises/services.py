# pylint: disable=line-too-long, too-many-locals, too-many-nested-blocks, too-many-branches

from parliament.models import Parliament, ParliamentSession
from promises.models import Promise, PromiseCase
from case_gather.models import Case
from subjects.models import CaseSubject, PromiseSubject
import parliament.services as ParliamentServices

def find_connected_bills_and_promises():
    current_parliament = Parliament.objects.latest('created')
    parliament_sessions_ids = ParliamentServices.parliament_session_ids_by_parliament(current_parliament)
    current_promises = Promise.objects.filter(parliament=current_parliament.id) 
    cases_in_sessions = Case.objects.filter(session_id__in=parliament_sessions_ids)

    for case in cases_in_sessions:
        case_subject_ids = CaseSubject.objects
            .filter(case=case)
            .values_list('id', flat=True)
        
        # We look at each promise within the same parliament session
        for promise in current_promises:
            promise_subject_ids = PromiseSubject.objects
                .filter(promise=promise)
                .values_list('id', flat=True)

            if case_subject_ids and promise_subject_ids:
                # We make sure the case and the promise have subjects
                if len(promise_subject_ids) > 4:
                    # We want at least 4 subjects on the promise

                    number_of_common_subjects = 0
                    for promise_subject_id in promise_subject_ids:
                        # We go through the case subject ids and find any common subjects
                        # in the promise subject id array
                        if promise_subject_id in case_subject_ids:
                            number_of_common_subjects += 1

                    # If the percent between common subjects and the largest array
                    # reaches a certain point we want to connect the case and promise. If
                    number_of_common_subjects_float = float(number_of_common_subjects)
                    number_of_promise_subjects_float = float(len(promise_subject_ids))
                    percent_of_common_subjects = (number_of_common_subjects_float / number_of_promise_subjects_float) * 100
                    
                    # If the percent is 80% or higher we make a connection
                    if percent_of_common_subjects >= 0.8:
                        PromiseCase.objects.create(
                            case=case,
                            promise=promise,
                            relationship_type='Connected',
                            percent_of_common_subjects=percent_of_common_subjects,
                        )
                    # If the percent is between 50% and 79% we create a suggested connection
                    elif percent_of_common_subjects >= 0.5:
                        PromiseCase.objects.create(
                            case=case,
                            promise=promise,
                            relationship_type='Suggested',
                            percent_of_common_subjects=percent_of_common_subjects,
                        )
