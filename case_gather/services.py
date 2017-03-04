#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case
from parliament.models import ParliamentSession
import case_gather.xml_parser as xml_parser

# TODO: update Subjects in db


def update_case_db(session_number):
    logger = logging.getLogger('cronJobServices')
    logger.info('update started')

    logger.info('getting parliament session object')
    parliament_session = ParliamentSession.objects.get(
        session_number=session_number)

    try:
        cases_in_db = Case.objects.filter(
            parliament_session=parliament_session)
        logger.info(cases_in_db)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-' +
                     e.message, traceback.format_exc())

    logger.info('Have cases in database')

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)
    logger.info('Following are case numbers already in db')
    logger.info(case_numbers)
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
    #  'rel_cases', 'subjects', 'session'
    logger.info('Starting to iterate over cases')
    for case in new_cases:
        logger.info('iteration in progress')
        logger.info(case)
        if int(case['number']) in case_numbers:
            logger.info('case is already in db')
        else:
            logger.info('Creating case')

            try:
                Case.objects.create(name=case['name'],
                                    number=int(case['number']),
                                    parliament_session=parliament_session,
                                    case_type=case['case_type'],
                                    case_status=case['case_status'])
            except Exception as e:
                logger.error(e.message)
                logger.info('case creation failure')
            logger.info('Case entry created')

    new_cases.close()
    logger.info('case has been closed')
