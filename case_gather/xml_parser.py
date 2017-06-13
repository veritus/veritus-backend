#!/usr/bin/python
# pylint: disable=line-too-long, lost-exception
import logging
import requests
from bs4 import BeautifulSoup

import case_gather.xml_helper as xml_helper

XML_LOGGER = logging.getLogger('xmlParser')

def get_case_data(parliament_session_number):
    # Combines xml_helper.get_case_details and
    # xml_helper.get_case_summary into a list
    # that will suffice to create a Case object for database
    # summary : [goal, changes, law_changes, costs, resolution]
    # details : [status, rel_cases, subj_ids]
    # output has keys: number, name, case_type, althingi_status, rel_cases, subjects, sessions
    XML_LOGGER.info('Getting case data from get_cases')
    case = get_cases(parliament_session_number)
    # used keys at this point:
    # number, session, name, case_type, althingi_status, rel_cases, subjects
    # more can be added as models are changed or added

    link_details = """http://www.althingi.is/altext/xml/thingmalalisti/thingmal/?lthing=%i&malnr=""" % parliament_session_number
    
    for number, name, case_type, althingi_link in case:
        XML_LOGGER.info('Looking at case: ' + name)
        try:
            details_soup = get_xml(link_details + str(number))
            XML_LOGGER.info('Got details soup for: ' + name)
        except Exception as e:
            XML_LOGGER.info('get_case_data failed with error: ' + e)

        try:
            details = xml_helper.get_case_details(details_soup)
            XML_LOGGER.info('Got details data for: ' + name)
            XML_LOGGER.info(details)
        except Exception as e:
            XML_LOGGER.error(e.message)
            XML_LOGGER.info('could not parse soup')


        althingi_status = details[0]
        rel_cases = details[1]
        subjects = details[2]
        case_creator_names = details[3]

        output = {
            'number': number,
            'name': name,
            'rel_cases': rel_cases,
            'case_type': case_type,
            'session': parliament_session_number,
            'althingi_status': althingi_status,
            'subjects': subjects,
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
    soup = get_xml(link + subject_id)

    output = {}

    try:
        group_number = xml_helper.get_attribute_value(
            soup, "yfirflokkur", "id")
        assert group_number is None
    except:
        XML_LOGGER.info('No subject found at number: ' + subject_id)
    else:
        text = xml_helper.get_element_text(soup, "heiti")

        group_name = next(text)
        subject_name = next(text)
        subject_description = next(text)

        cases = xml_helper.get_attribute_value(soup, "mál", "málsnúmer")

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


def get_subjects():
    """
    Function to yield from get_subjects
    Format of output is [subject_id, group_name, subject_name,
                                        subject_description, case_numbers]
    """
    for i in range(1, 100):
        output = get_subject(i)
        if output is not None:
            yield output
        else:
            pass


def get_cases(parliament_session_number):
    """
    Function (generator) to retrieve a case from þingmálalisti
    Interesting information:
        - Case number
        - Case name
        - Case type ( single letter identifier)

    Output format: [case_number, case_name, case_type]
    """
    XML_LOGGER.info('Starting get_cases')

    cases = case_collector(parliament_session_number)
    XML_LOGGER.info('Cases have been collected')
    try:
        for number, name, case_type, althingi_link in cases:
            output = [number, name, case_type, althingi_link]
            yield output
    except Exception as e:
        XML_LOGGER.error(e.message)
        XML_LOGGER.info('Iteration over all parliament cases complete')


def case_collector(parliament_session_number):

    link = "http://www.althingi.is/altext/xml/thingmalalisti/?lthing="
    soup = get_xml(link + str(parliament_session_number))
    XML_LOGGER.info('have the case soup')

    # Gets number for case
    case_numbers_gen = xml_helper.get_attribute_value(
        soup, "mál", "málsnúmer"
    )
    XML_LOGGER.info('have the case numbers generator')

    # Gets case name
    case_names_gen = xml_helper.get_element_text(soup, "málsheiti")
    XML_LOGGER.info('have the case names generator')

    # Gets case type
    case_types_gen = xml_helper.get_attribute_value(
        soup, "málstegund", "málstegund"
    )
    XML_LOGGER.info('have the case case_types_gen generator')

    # Link to case on althingi.is is in an element called html
    althingi_link_gen = xml_helper.get_element_text(
        soup, "html"
    )
    XML_LOGGER.info('have the case althingi_link_gen generator')

    for number, name, case_type, althingi_link in zip(case_numbers_gen, case_names_gen, case_types_gen, althingi_link_gen):
        yield number, name, case_type, althingi_link


def get_xml(link):
    try:
        result = requests.get(link)
    except Exception as e:
        XML_LOGGER.error(e.message)
    else:
        content = result.content
        soup = BeautifulSoup(content, features="xml")
        return soup
    finally:
        pass
