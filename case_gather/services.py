#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case
import case_gather.xml_parser as xml_parser
from parliament.models import ParliamentSession

CRONLOGGER = logging.getLogger('cronJobServices')

def update_case_db(session_number):
    CRONLOGGER.info('update started')

    parliament_session = ParliamentSession.objects.get(
        session_number=session_number
    )

    cases_in_db = Case.objects.filter(
        parliament_session=parliament_session
    )
    CRONLOGGER.info(cases_in_db)

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    try:
        new_cases = xml_parser.get_case_data(session_number)
    except Exception as e:
        CRONLOGGER.error(e.message + '-' + traceback.format_exc())

    #  Case has keys:
    #  'number', 'name', 'case_type', 'case_status'
    #  'rel_cases', 'subjects', 'session'
    for case in new_cases:
        CRONLOGGER.info(case)
        if int(case['number']) in case_numbers:
            CRONLOGGER.info('case is already in db')
        else:
            CRONLOGGER.info('Creating case')

            try:
                Case.objects.create(name=case['name'],
                                    number=int(case['number']),
                                    parliament_session=parliament_session,
                                    case_type=case['case_type'],
                                    case_status=case['case_status'])
            except Exception as e:
                CRONLOGGER.error(e.message)
                CRONLOGGER.error('case creation failure')
            CRONLOGGER.info('Case entry created')

    new_cases.close()
    CRONLOGGER.info('update finished')
