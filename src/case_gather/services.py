#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case, CaseCreator, AlthingiStatusToStatusMapper, Subject
import case_gather.xml_parser as xml_parser
from parliament.models import ParliamentSession, ParliamentMember
from subjects.models import CaseSubject

CRONLOGGER = logging.getLogger('cronJobServices')

def update_case_db(session_number):
    CRONLOGGER.info('Updating case database started')
    
    try:
        new_cases = xml_parser.get_case_data(session_number)
    except Exception as e:
        CRONLOGGER.error(e.message + '-' + traceback.format_exc())


    parliament_session = ParliamentSession.objects.get(
        session_number=session_number
    )

    # We retrieve all current cases to see if we need to create
    # or update
    cases_in_db = Case.objects.filter(
        parliament_session=parliament_session
    )

    case_numbers = []
    for case in cases_in_db:
        case_numbers.append(case.number)

    althingi_status_to_status_map = create_althingi_status_to_status_map()

    for case in new_cases:
        #  Case has keys:
        #  'number', 'name', 'case_type', 'althingi_status'
        #  'rel_cases', 'subjects', 'session'
        CRONLOGGER.info('Starting to create/update case: ')
        CRONLOGGER.info(case)
        if int(case['number']) in case_numbers:
            CRONLOGGER.info('case is already in db')
        else:
            CRONLOGGER.info('Creating case')

            # We find the status from the althingi status
            althingi_status = case['althingi_status']
            status = 'Unknown'
            if althingi_status in althingi_status_to_status_map:
                status = althingi_status_to_status_map[althingi_status]

            try:
                new_case = Case.objects.create(
                    name=case['name'],
                    number=int(case['number']),
                    parliament_session=parliament_session,
                    case_type=case['case_type'],
                    althingi_status=althingi_status,
                    althingi_link=case['althingi_link'],
                    status=status
                )
                create_subjects(parliament_session, new_case, case['subject_names'])
                CRONLOGGER.info('case creators')
                CRONLOGGER.info(case['case_creator_names'])
                for case_creator_name in case['case_creator_names']:
                    CRONLOGGER.info(case_creator_name)
                    parliament_member = ParliamentMember.objects.filter(name=case_creator_name)
                    if parliament_member.exists():
                        parliament_member = parliament_member.get()
                        CaseCreator.objects.create(
                            case=new_case,
                            parliament_member=parliament_member
                        )
                    else:
                        CRONLOGGER.error('Parliament member not found: ' + case_creator_name)
            except Exception as e:
                CRONLOGGER.error(e.message)
                CRONLOGGER.error('case creation failure')
            CRONLOGGER.info('Case entry created')

    new_cases.close()
    CRONLOGGER.info('update finished')


def create_althingi_status_to_status_map():
    # Creates a map so that we can easily retrieve the status from the
    # althingi_status. This is done as the althingi status is too complicated
    # Key and Value are stored in database
    # Map will look something like:
    # {
    #    "": "Unknown",
    #    "Samþykkt sem lög frá Alþingi.": "Passed",
    #    "Í nefnd eftir 1. umræðu.": "In progess",
    #    "Bíður 1. umræðu.": "In progess",
    #    "Bíður 2. umræðu": "In progress",
    #    "Vísað til ríkisstjórnar.": "In progress"
    #    "Fyrirspurnin var felld niður vegna ráðherraskipta.": "Rejected",
    #    "Fyrirspurninni var svarað skriflega.": "Answered",
    #    "Fyrirspurninni var svarað munnlega.": "Answered",
    #    "Fyrirspurninni hefur ekki verið svarað.": "Has not been answered",
    #    "Fyrirspurnin var kölluð aftur.": "Withdrawn",
    # }
    althingi_status_to_status = AlthingiStatusToStatusMapper.objects.all()
    althingi_status_to_status_map = {}
    for status_map in althingi_status_to_status:
        althingi_status_to_status_map[status_map.althingi_status] = status_map.status
    return althingi_status_to_status_map


def create_subjects(parliament_session, case, subjects):
    # Case is case object
    # Subjects is array of strings (subjects)
    CRONLOGGER.info('create subjects')
    CRONLOGGER.info(case)
    CRONLOGGER.info(subjects)
    for subject_name in subjects:
        subject = Subject.objects.filter(name=subject_name)
        if not subject.exists():
            CRONLOGGER.info('creating new subject')
            subject = Subject.objects.create(
                parliament_session=parliament_session,
                name=subject_name
            )
        else:
            subject = subject.get()
        CRONLOGGER.info('creating new CaseSubject')
        CaseSubject.objects.create(
            case=case,
            subject=subject
        )
