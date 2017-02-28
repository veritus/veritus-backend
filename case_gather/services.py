#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case  # , Subject
from parliament.models import ParliamentSession
import case_gather.xml_parser

logger = logging.getLogger('cronJobServices')


def update_case_db(session_number):

    try:
        cases_in_db = Case.objects.filter(
            parliament_session=session_number)
    except Exception as e:
        logger.error('Failed to create objects, error raised:', e.message, traceback.format_exc())
    
    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    try:
        new_cases = xml_parser.get_case_data(session_number)
    except Exception as e:
        logger.error(e.message, traceback.format_exc())

    #  Case has keys:
    #  'number', 'name', 'case_type', 'case_status'
    #  'rel_cases', 'subjects', 'sessions'

    try:
        case = next(new_cases)
        logger.info('getting next case', case[0])
        assert int(case['number']) not in case_numbers
    except Exception as e:
        logger.info('Case', case['number'], 'already in db')
        logger.info('Debugging info:', e)
    else:
        logger.info('Creating case number: ' + str(case['number']))
        Case.objects.create(name=case['name'],
                            number=case['number'],
                            parliament_session=case['sessions'],
                            case_type=case['case_type'],
                            case_status=case['case_status'])
        # related_case_numbers=case['rel_cases'],
        # subject_numbers=case['subjects'])
    finally:
        new_cases.close()
