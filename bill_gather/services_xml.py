#!/usr/bin/python
import logging
from bill_gather.models import Case  # , Subject
from parliament.models import ParliamentSession
from xml_parser import get_case_data  # get_subjects,

cron_logger = logging.getLogger('cronJobs')


def update_case_db(session_number):

    parliament_session = ParliamentSession.objects.get(
        session_number=session_number)

    cases_in_db = Case.objects.filter(
        parliament_session=parliament_session)

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    new_cases = get_case_data(session_number)
    # output has keys: 'number', 'name', 'case_type', 'case_status', 'rel_cases'
    #                             'subjects', 'sessions'

    try:
        case = next(new_cases)
        assert int(case['number']) not in case_numbers
    except:
        pass
    else:
        cron_logger.info('Creating case number: ' + str(case['number']))
        Case.objects.create(name=case['name'],
                            number=case['number'],
                            parliament_session=case['sessions'],
                            case_type=case['case_type'],
                            case_status=case['case_status'])
                            # related_case_numbers=case['rel_cases'],
                            # subject_numbers=case['subjects'])
