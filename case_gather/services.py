#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case  # , Subject
from parliament.models import ParliamentSession
import case_gather.xml_parser as xml_parser


def update_case_db(session_number):
    logger = logging.getLogger('cronJobServices')
    logger.info('update started')

    try:
        cases_in_db = Case.objects.filter(
            parliament_session=session_number)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-'
                     + e.message, traceback.format_exc())

    # logger.info('Have cases in database')

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    # logger.info('have list of case numbers')

    try:
        logger.info('scraping for new cases')
        new_cases = xml_parser.get_case_data(session_number)
        logger.info('have a new_cases object')
    except Exception as e:
        logger.error(e.message + '-' + traceback.format_exc())
        logger.info('There was an error')

    #  Case has keys:
    #  'number', 'name', 'case_type', 'case_status'
    #  'rel_cases', 'subjects', 'sessions'

    try:
        logger.info('have new case')
        for case in new_cases:
            logger.info('getting next case' + '-' + str(case['number']))
            assert int(case['number']) in case_numbers
            logger.info('case is already in db')
    except Exception as e:
        logger.info('Case' + str(case['number']) + 'already in db')
        logger.info('Debugging info:' + e)
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
        logger.info('case has been closed')
