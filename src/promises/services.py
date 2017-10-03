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
    cases_in_sessions = Case.objects.filter(parliament_session__in=parliament_sessions_ids)

    for case in cases_in_sessions:
        case_subject_ids = CaseSubject.objects.filter(case=case).values_list('id', flat=True)
        
        # We look at each promise within the same parliament
        for promise in current_promises:
            promise_subject_ids = PromiseSubject.objects.filter(promise=promise).values_list('id', flat=True)

            if len(promise_subject_ids) > 4:
                # We want more than 4 subjects on the promise

                case_subject_set = set(case_subject_ids)
                promise_subject_set = set(promise_subject_ids)
                # We use set intersection to determine the number of common subjects
                number_of_common_subjects = len(case_subject_set.intersection(promise_subject_set))

                number_of_common_subjects_float = float(number_of_common_subjects)
                number_of_promise_subjects_float = float(len(promise_subject_ids))
                percent_of_common_subjects = (number_of_common_subjects_float / number_of_promise_subjects_float) * 100
                
                # If the percent is 80% or higher we make a connection
                if percent_of_common_subjects >= 80:
                    PromiseCase.objects.create(
                        case=case,
                        promise=promise,
                        relationship_type='Connected',
                        percent_of_common_subjects=percent_of_common_subjects,
                    )
                # If the percent is between 50% and 79% we create a suggested connection
                elif percent_of_common_subjects >= 50:
                    PromiseCase.objects.create(
                        case=case,
                        promise=promise,
                        relationship_type='Suggested',
                        percent_of_common_subjects=percent_of_common_subjects,
                    )
