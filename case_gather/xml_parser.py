#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import logging

import case_gather.xml_helper as xml_helper


def get_case_data(parliament_session_number):
    xml_logger = logging.getLogger('xmlParser')
    """
    Combines xml_helper.get_case_details and
    xml_helper.get_case_summary into a list
    that will suffice to create a Case object for database
    summary : [goal, changes, law_changes, costs, resolution]
    details : [status, rel_cases, subj_ids]
    output has keys: 'number', 'name', 'case_type', 'case_status', 'rel_cases'
                                'subjects', 'sessions'
    """
    # TODO
    # link_summary = "http://www.althingi.is/altext/xml/samantektir\
    #     /samantekt/?lthing=146&malnr="

    link_details = """http://www.althingi.is/altext/xml/thingmalalisti/thingmal/?lthing=%i&malnr=""" % parliament_session_number
    xml_logger.info('Getting case data from get_cases')
    case = get_cases(parliament_session_number)

    # used keys at this point:
    # number, session, name, case_type, case_status, rel_cases, subjects
    # more can be added as models are changed or added

    output = {}

    for number, name, case_type in case:
        # TODO
        # summary_soup = get_xml(link_summary + str(number))

        try:
            details_soup = get_xml(link_details + str(number))
        except Exception as e:
            xml_logger.info('get_case_data failed with error: ' + e)

        try:
            details = xml_helper.get_case_details(details_soup)

        # TODO
        # summary = xml_helper.get_case_summary(summary_soup)

        except Exception as e:
            xml_logger.error(e.message)
            xml_logger.info('could not parse soup')

        case_status = details[0]
        rel_cases = details[1]
        subjects = details[2]

        output = {'number': number, 'name': name, 'rel_cases': rel_cases,
                  'case_type': case_type, 'session': parliament_session_number,
                  'case_status': case_status, 'subjects': subjects}

        yield output


def get_subject(subject_id):
    xml_logger = logging.getLogger('xmlParser')
    """
    Function to extract information about subjects (efnisflokkur)
    Interesting information:
     - Major group number
     - Major group name
     - subject number
     - subject name
     - subject description
     - case numbers associated with subject
    output keys: [subject_id, group_name, subject_name,
             subject_description, case_numbers]
    """
    link = "http://www.althingi.is/altext/xml/efnisflokkar/efnisflokkur/?efnisflokkur="
    soup = get_xml(link + subject_id)

    output = {}

    try:
        group_number = xml_helper.get_attribute_value(
            soup, "yfirflokkur", "id")
        assert group_number is None
    except:
        xml_logger.info('No subject found at number:', subject_id)
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
        output = {'id': subject_id,
                  'group_name': group_name,
                  'name': subject_name,
                  "description": subject_description,
                  "case_numbers": case_numbers}
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
    xml_logger = logging.getLogger('xmlParser')
    xml_logger.info('starting get_cases')

    cases = case_collector(parliament_session_number)

    try:
        for number, name, case_type in cases:
            output = [number, name, case_type]
            yield output
    except Exception as e:
        xml_logger.error(e.message)
        xml_logger.info('Iteration over all parliament cases complete')


def case_collector(parliament_session_number):
    xml_logger = logging.getLogger('xmlParser')

    link = "http://www.althingi.is/altext/xml/thingmalalisti/?lthing="
    soup = get_xml(link + str(parliament_session_number))

    xml_logger.info('have the case soup')

    case_numbers_gen = xml_helper.get_attribute_value(
        soup, "mál", "málsnúmer")

    xml_logger.info('have the case numbers generator')

    case_names_gen = xml_helper.get_element_text(soup, "málsheiti")

    xml_logger.info('have the case names generator')

    case_types_gen = xml_helper.get_attribute_value(
        soup, "málstegund", "málstegund")

    xml_logger.info('have the case case_types_gen generator')

    for number, name, case_type in zip(case_numbers_gen, case_names_gen, case_types_gen):
        yield number, name, case_type


def get_xml(link):
    xml_logger = logging.getLogger('xmlParser')
    try:
        result = requests.get(link)
    except Exception as e:
        xml_logger.error(e.message)
    else:
        content = result.content
        soup = BeautifulSoup(content, features="xml")
        return soup
    finally:
        pass
