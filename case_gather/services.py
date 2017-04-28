#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case
from parliament.models import ParliamentSession
import case_gather.xml_parser as xml_parser


def update_case_db(session_number):
    logger = logging.getLogger('cronJobServices')
    logger.info('update started')

    parliament_session = ParliamentSession.objects.get(
        session_number=session_number)

    try:
        cases_in_db = Case.objects.filter(
            parliament_session=parliament_session)
        logger.info(cases_in_db)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-' +
                     e.message, traceback.format_exc())

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    try:
        new_cases = xml_parser.get_case_data(session_number)
    except Exception as e:
        logger.error(e.message + '-' + traceback.format_exc())

    #  Case has keys:
    #  'number', 'name', 'case_type', 'case_status'
    #  'rel_cases', 'subjects', 'session'
    for case in new_cases:
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
    logger.info('update finished')

def update_subject_db():
    logger = logging.getLogger('cronJobServices')
    logger.info('Subject update started')

    try:
        subjects_in_db = Subject.objects.all()
        logger.info(subjects_in_db)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-' +
                     e.message, traceback.format_exc())

    subject_number = []
    for subject in subjects_in_db:
        subject_numbers.append(subject.number)

    try:
        new_subjects = xml_parser.get_subject_data()
    except Exception as e:
        logger.error(e.message + '-' + traceback.format_exc())


    for subject in new_subjects:
        logger.info(subject)
        if int(subject['number']) in subject_numbers:
            logger.info('subject is already in db')
        else:
            logger.info('Creating subject')

            try:
                Subject.objects.create(parliament_session = self.parliament_session,
                                                name = self.subject_data['name'],
                                                parent = int(self.subject_data['parent']),
                                                number = self.subject_data['number'],
                                                description = self.subject_data['description'])
            except Exception as e:
                logger.error(e.message)
                logger.info('subject creation failure')
            logger.info('subject entry created')

    new_cases.close()
    logger.info('subject update finished')
    
