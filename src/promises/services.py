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
        case_subject_ids = CaseSubject.objects.filter(case=case).values_list('subject_id', flat=True)

        # We look at each promise within the same parliament
        for promise in current_promises:
            promise_subject_ids = PromiseSubject.objects.filter(promise=promise).values_list('subject_id', flat=True)
            if len(promise_subject_ids) > 4:
                # We only want to look at promises that have enough subjects
                # This is because we want sufficient depth when looking at the relation
                # between promise and case to improve the quality of each connection.
                # This is because we dont want to match a case and a promise just because they share
                # one subject, as they might still be very different and not related at all.
                # However, a case and promise that share 5 subjects, are likely related.
                case_subject_set = set(case_subject_ids)
                promise_subject_set = set(promise_subject_ids)
                # We use set intersection to determine the number of common subjects
                number_of_common_subjects = len(case_subject_set.intersection(promise_subject_set))
                number_of_common_subjects_float = float(number_of_common_subjects)
                number_of_promise_subjects_float = float(len(promise_subject_ids))
                percent_of_common_subjects = (number_of_common_subjects_float / number_of_promise_subjects_float) * 100

                # If the case and promise share a certain percentage of subjects
                # then we create a connection between them
                if percent_of_common_subjects >= 50:
                    relationship_type = 'Suggested'
                    if percent_of_common_subjects >= 80:
                        relationship_type = 'Connected'
                    
                    # We check if the connection already exists
                    case_promise_connection = PromiseCase.objects.filter(case=case, promise=promise)
                    if case_promise_connection.exists():
                        # We update the percentage if the connection exists
                        case_promise_connection = case_promise_connection.get()
                        case_promise_connection.percent_of_common_subjects = percent_of_common_subjects
                        case_promise_connection.save()
                    else:
                        # If the connection does not exist already, we create one
                        PromiseCase.objects.create(
                            case=case,
                            promise=promise,
                            relationship_type=relationship_type,
                            percent_of_common_subjects=percent_of_common_subjects,
                        )
