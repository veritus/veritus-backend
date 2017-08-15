#!/usr/bin/python
# pylint: disable=line-too-long, lost-exception
import logging
import requests
from bs4 import BeautifulSoup

import soupUtils

XML_LOGGER = logging.getLogger('xmlParser')

def get_case_data(parliament_session_number):
    """
    Combines get_case_details and get_case_summary into a list
    that will suffice to create a Case object for database
    """

    XML_LOGGER.info('Getting case data from get_cases')
    # Gets all cases with some limited data
    case = get_cases(parliament_session_number)

    link_details = """http://www.althingi.is/altext/xml/thingmalalisti/thingmal/?lthing=%i&malnr=""" % parliament_session_number

    for number, name, case_type, althingi_link in case:
        # Go through cases and get more details from them
        XML_LOGGER.info('Looking at case: ' + name)
        details_soup = soupUtils.getSoupFromLink(link_details + str(number))
        XML_LOGGER.info('Got details soup for: ' + name)

        # We go to the details page of the case and get more data
        details = get_case_details(details_soup)
        XML_LOGGER.info('Got details data for: ' + name)
        XML_LOGGER.info(details)

        althingi_status = details[0]
        rel_cases = details[1]
        subject_names = details[2]
        case_creator_names = details[3]

        output = {
            'number': number,
            'name': name,
            'rel_cases': rel_cases,
            'case_type': case_type,
            'session': parliament_session_number,
            'althingi_status': althingi_status,
            'subject_names': subject_names,
            'althingi_link': althingi_link,
            'case_creator_names': case_creator_names
        }

        yield output


def get_subject(subject_id):
    #  Function to extract information about subjects (efnisflokkur)
    # Interesting information:
    #  - Major group number
    #  - Major group name
    #  - subject number
    #  - subject name
    #  - subject description
    #  - case numbers associated with subject
    # output keys: [subject_id, group_name, subject_name,
    #          subject_description, case_numbers]

    link = 'http://www.althingi.is/altext/xml/efnisflokkar/efnisflokkur/?efnisflokkur='
    soup = soupUtils.getSoupFromLink(link + subject_id)

    output = {}

    try:
        group_number = soupUtils.get_attribute_value(
            soup, "yfirflokkur", "id")
        assert group_number is None
    except:
        XML_LOGGER.info('No subject found at number: ' + subject_id)
    else:
        text = soupUtils.get_element_text(soup, "heiti")

        group_name = next(text)
        subject_name = next(text)
        subject_description = next(text)

        cases = soupUtils.get_attribute_value(soup, "mál", "málsnúmer")

        # Build list of case numbers
        case_numbers = []
        for number in cases:
            case_numbers.append(number)

        # Sort the case numbers
        case_numbers.sort()
        output = {
            'id': subject_id,
            'group_name': group_name,
            'name': subject_name,
            "description": subject_description,
            "case_numbers": case_numbers
        }
    finally:
        group_number.close()
        text.close()
        cases.close()
        return output


def get_cases(parliament_session_number):

    """
    Function (generator) to retrieve a case from þingmálalisti
    Interesting information:
        - Case number
        - Case name
        - Case type ( single letter identifier)
        - Althingi_link (link to case on athingi.is)

    Output format: [case_number, case_name, case_type]
    """
    XML_LOGGER.info('Starting get_cases')

    cases = case_collector(parliament_session_number)

    XML_LOGGER.info('Cases have been collected')
    for number, name, case_type, althingi_link in cases:
        output = [number, name, case_type, althingi_link]
        yield output



def case_collector(parliament_session_number):

    link = "http://www.althingi.is/altext/xml/thingmalalisti/?lthing="
    soup = soupUtils.getSoupFromLink(link + str(parliament_session_number))
    XML_LOGGER.info('have the case soup')

    # Gets number for case
    case_numbers_gen = soupUtils.get_attribute_value(
        soup, "mál", "málsnúmer"
    )
    XML_LOGGER.info('have the case numbers generator')

    # Gets case name
    case_names_gen = soupUtils.get_element_text(soup, "málsheiti")
    XML_LOGGER.info('have the case names generator')

    # Gets case type
    case_types_gen = soupUtils.get_attribute_value(
        soup, "málstegund", "málstegund"
    )
    XML_LOGGER.info('have the case case_types_gen generator')

    # Link to case on althingi.is is in an element called html
    althingi_link_gen = soupUtils.get_element_text(
        soup, "html"
    )
    XML_LOGGER.info('have the case althingi_link_gen generator')

    for number, name, case_type, althingi_link in zip(case_numbers_gen, case_names_gen, case_types_gen, althingi_link_gen):
        yield number, name, case_type, althingi_link


def get_case_details(soup):
    """
    Function to retrieve case information from þingmál
    Interesting information:
        - Case status (if a law) (staðamáls)
        - Related case numbers (mál : málsnúmer)
        - subject id numbers (efnisflokkur : id)
    Output format [status, rel_casenumber, id_numbers]
    """
    XML_LOGGER.info('starting get_case_details')

    status_flag = True
    try:
        status_gen_ = soupUtils.get_element_text(soup, "staðamáls")
        test = next(status_gen_)
        assert test is not None
        status_gen = soupUtils.get_element_text(soup, 'staðamáls')
    except:
        XML_LOGGER.info('Case has no status')
        status_flag = False

    # Get case creators
    case_creators_element = soup.findAll('framsögumenn')
    case_creators_names = []
    for case_creator_element in case_creators_element:
        name = next(soupUtils.get_element_text(case_creator_element, 'nafn'))
        case_creators_names.append(name)
    XML_LOGGER.info(case_creators_names)

    # Get related cases
    rel_cases_gen = soupUtils.get_attribute_value(soup, "mál", "málsnúmer")
    rel_cases = []
    for rel_case in rel_cases_gen:
        rel_cases.append(rel_case)

    # remove the first rel_case, as it is the actual case
    rel_cases.pop(0)

    # Get case subjects
    subjects_root_element = soup.find('efnisflokkar')
    subject_names_gen = soupUtils.get_element_text(subjects_root_element, "heiti")
    subject_names = []
    for name in subject_names_gen:
        subject_names.append(name)

    if status_flag:
        status = next(status_gen)
    else:
        status = ''

    output = [
        status,
        rel_cases,
        subject_names,
        case_creators_names
    ]
    return output

def get_case_summary(soup):
    """
    Function to retrieve case information from samantekt
    Interesting information:
        - Goal (markmið)
        - Significant changes (helstuBreytingar)
        - law changes (breytingaráLögum)
        - costs and income (kostnaðurOgTekjur)
        - (afgreiðsla)
    output format [goal, sign_changes, law_changes, costs, resolution]
    """
    XML_LOGGER.info('starting get_case_summary')

    goal_gen = soupUtils.get_element_text(soup, "markmið")
    changes_gen = soupUtils.get_element_text(soup, "helstuBreytingar")
    law_changes_gen = soupUtils.get_element_text(soup, "breytingaráLögum")
    costs_gen = soupUtils.get_element_text(soup, "kostnaðurOgTekjur")
    resolution_gen = soupUtils.get_element_text(soup, "afgreiðsla")

    goal = next(goal_gen)
    changes = next(changes_gen)
    law_changes = next(law_changes_gen)
    costs = next(costs_gen)
    resolution = next(resolution_gen)

    output = [goal, changes, law_changes, costs, resolution]
    return output
