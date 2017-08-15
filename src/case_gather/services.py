#!/usr/bin/python
import logging
import traceback
from case_gather.models import Case, CaseCreator, AlthingiStatusToStatusMapper, Subject
import case_gather.xml_parser as xml_parser
from parliament.models import ParliamentSession, ParliamentMember
from subjects.models import CaseSubject
import main.sentryLogger as sentryLogger

CRONLOGGER = logging.getLogger('cronJobServices')

def update_cases_by_session_number(session_number):
    """
    Takes in a session number Integer, scrapes the althingi.is website
    and creates new Cases and relevant information from the data
    """
    parliament_session = ParliamentSession.objects.get(
        session_number=session_number
    )

    case_numbers = get_current_case_numbers_by_parliament_session(parliament_session)

    althingi_status_to_status_map = create_althingi_status_to_status_map()

    new_cases = xml_parser.get_case_data(session_number)
    for case in new_cases:
        #  Case has keys:
        #  'number', 'name', 'case_type', 'althingi_status'
        #  'rel_cases', 'subjects', 'session'
        CRONLOGGER.info('Starting to create/update case: ')
        CRONLOGGER.info(case)

        if int(case['number']) not in case_numbers:
            # If the case does not exist, we create it
            CRONLOGGER.info('Creating case')

            # We find the status from the althingi status
            althingi_status = case['althingi_status']

            new_case = Case.objects.create(
                name=case['name'],
                number=int(case['number']),
                parliament_session=parliament_session,
                case_type=case['case_type'],
                althingi_status=althingi_status,
                althingi_link=case['althingi_link'],
                status=getCaseStatus(althingi_status)
            )

            create_subjects(parliament_session, new_case, case['subject_names'])

            createCaseCreators(case['case_creator_names'], new_case)            
            
    new_cases.close()


def get_current_case_numbers_by_parliament_session(parliament_session):
    """
    Takes in a parliament_session, retrieves the cases connected to it
    from the database and returns their ids
    """
    current_cases = Case.objects.filter(
        parliament_session=parliament_session
    )

    case_numbers = []
    for case in current_cases:
        case_numbers.append(case.number)
    return case_numbers


def getCaseStatus(althingi_status):
    """
    Takes in althingi_status (see: create_althingi_status_to_status_map())
    and either returns the status we have defined to be equivalent 
    or returns Unknown as a default
    """
    if althingi_status in althingi_status_to_status_map:
        return althingi_status_to_status_map[althingi_status]
    else
        # Default status if the althingi status is not found in our database
        return 'Unknown'


def createCaseCreators(case_creator_names, case):
    """
    Takes in an array of strings which are names 
    Takes in a case, which is a Case object
    It finds the ParliamentMember who has that name
    and creates a CaseCreator object from the ParliamentMember
    and the inputted Case.
    If the ParliamentMember is not found, we log to Sentry as then
    a new one has to be created in the database
    """
    for case_creator_name in case_creator_names:
        parliament_member = ParliamentMember.objects.filter(name=case_creator_name)
        if parliament_member.exists():
            parliament_member = parliament_member.get()
            CaseCreator.objects.create(
                case=case,
                parliament_member=parliament_member
            )
        else:
            sentryLogger.logToSentry('Parliament member not found: ' + case_creator_name)

def create_althingi_status_to_status_map():
    """
     Creates a map so that we can easily retrieve a more readable status from the
     althingi_status. This is done as the althingi status is too complicated.
     Key and Value are stored in database
     Map will look something like:
     {
        "": "Unknown",
        "Samþykkt sem lög frá Alþingi.": "Passed",
        "Í nefnd eftir 1. umræðu.": "In progess",
        "Bíður 1. umræðu.": "In progess",
        "Bíður 2. umræðu": "In progress",
        "Vísað til ríkisstjórnar.": "In progress"
        "Fyrirspurnin var felld niður vegna ráðherraskipta.": "Rejected",
        "Fyrirspurninni var svarað skriflega.": "Answered",
        "Fyrirspurninni var svarað munnlega.": "Answered",
        "Fyrirspurninni hefur ekki verið svarað.": "Has not been answered",
        "Fyrirspurnin var kölluð aftur.": "Withdrawn",
     }
     These statuses can also be found in the init_data.json file.
    """
    althingi_status_to_status = AlthingiStatusToStatusMapper.objects.all()
    althingi_status_to_status_map = {}
    for status_map in althingi_status_to_status:
        althingi_status_to_status_map[status_map.althingi_status] = status_map.status
    return althingi_status_to_status_map


def create_subjects(parliament_session, case, subjects):
    """
    Takes in a parliament session Integer
    Takes in case Case object
    Takes in array of string subject names
    Creates a new Subject if the subject name is not found
    then creates a new CaseSubject connection to connect
    the Case and the Subject together.
    """
    # Case is case object
    # Subjects is array of strings (subjects)

    for subject_name in subjects:
        subject = Subject.objects.filter(name=subject_name)
        if not subject.exists():
            subject = Subject.objects.create(
                parliament_session=parliament_session,
                name=subject_name
            )
        else:
            subject = subject.get()
        CaseSubject.objects.create(
            case=case,
            subject=subject
        )
