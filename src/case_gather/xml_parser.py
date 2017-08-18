#!/usr/bin/python
# pylint: disable=line-too-long, lost-exception
import case_gather.soupUtils as soupUtils

def get_case_data(parliament_session_number):
    """
        Returns relevant case data. First getting all cases from one link
        and then finally visiting the details page of each case and
        harvesting data there.
    """
    # Gets all cases with some limited data
    link = "http://www.althingi.is/altext/xml/thingmalalisti/?lthing="
    cases_soup = soupUtils.getSoupFromLink(link + str(parliament_session_number))
    cases = collectCases(cases_soup)

    link_details = """http://www.althingi.is/altext/xml/thingmalalisti/thingmal/?lthing=%i&malnr=""" % parliament_session_number
    cases_data = []
    for number, name, case_type, althingi_link in cases:
        # Go through cases and get more details from them
        details_soup = soupUtils.getSoupFromLink(link_details + str(number))

        case = {
            'number': number,
            'name': name,
            'rel_cases': getRelatedCases(details_soup),
            'case_type': case_type,
            'session': parliament_session_number,
            'althingi_status': getStatus(details_soup),
            'subject_names': getSubjectNames(details_soup),
            'althingi_link': althingi_link,
            'case_creator_names': getCaseCreatorNames(details_soup)
        }
        cases_data.append(case)

    return cases_data

def collectCases(soup):
    """
        Collects cases from the soup
        Interesting information:
            - Case number
            - Case name
            - Case type ( single letter identifier)
            - Althingi_link (link to case on athingi.is)
    """

    cases = []
    for case in getAllCases(soup):
        number = getCaseNumberFromCase(case)
        name = getCaseName(case)
        case_type = getCaseType(case)
        althingi_link = getAlthingiLink(case)
        case = {
            'number': number,
            'name': name,
            'case_type': case_type,
            'althingi_link': althingi_link
        }
        cases.append(case)
    return cases

def getAllCases(soup):
    """
        Takes in a soup and returns all <mál><mál> tags
    """
    return soup.find_all('mál')

def getCaseNumberFromCase(soup):
    """
        Takes in a soup with <mál><mál> as the
        root tag and returns the málsnumer attribute
    """
    return soup["málsnúmer"]

def getCaseName(soup):
    """
        Takes in a soup and finds the case name
    """
    return soup.find("málsheiti").string

def getAlthingiLink(soup):
    """
        Takes in a soup and returns the althingi link under the html tag
    """
    return soup.find("html").string

def getCaseType(soup):
    """
        Takes in a soup and finds the name of the case type
    """
    return soup.find("málstegund").find('heiti').string

def getStatus(soup):
    """
        Takes in a soup and returns the status of the case
    """
    return soup.find("staðamáls").string


def getSubjectNames(soup):
    """
        Takes in a soup, finds all subjects and returns
        a list of their names
    """
    subject_names = []
    for subject_element in soup.find_all('efnisflokkur'):
        subject_name = subject_element.find("heiti").string
        subject_names.append(subject_name)
    return subject_names

def getRelatedCases(soup):
    """
        Takes in a soup and finds all relevant cases and returns
        their ids
    """
    related_cases = soupUtils.get_attribute_value(soup, "mál", "málsnúmer")

    # remove the first rel_case, as it is the actual case
    related_cases.pop(0)
    return related_cases

def getCaseCreatorNames(soup):
    """
        Takes in a soup and finds the 'framsögumenn'
        goes through them all, adds their names to a list
        and returns said list
    """
    case_creators_elements = soup.find_all("framsögumenn")
    #print(case_creators_elements)
    case_creators_names = []
    for case_creator_element in case_creators_elements:
        name = case_creator_element.find('nafn').string
        case_creators_names.append(name)
    return case_creators_names

#def get_case_summary(soup):
#    """
#    Function to retrieve case information from samantekt
#    Interesting information:
#        - Goal (markmið)
#        - Significant changes (helstuBreytingar)
#        - law changes (breytingaráLögum)
#        - costs and income (kostnaðurOgTekjur)
#        - (afgreiðsla)
#    output format [goal, sign_changes, law_changes, costs, resolution]
#    """
#    XML_LOGGER.info('starting get_case_summary')
#
#    goal = soupUtils.get_element_text(soup, "markmið")
#    changes = soupUtils.get_element_text(soup, "helstuBreytingar")
#    law_changes = soupUtils.get_element_text(soup, "breytingaráLögum")
#    costs = soupUtils.get_element_text(soup, "kostnaðurOgTekjur")
#    resolution = soupUtils.get_element_text(soup, "afgreiðsla")
#
#    return [
#        goal,
#        changes,
#        law_changes,
#       costs,
#       resolution
#   ]

#def get_subject(subject_id):
#    """
#    Function to extract information about subjects (efnisflokkur)
#    Interesting information:
#      - Major group number
#      - Major group name
#      - subject number
#      - subject name
#      - subject description
#      - case numbers associated with subject
#    output keys: [subject_id, group_name, subject_name, subject_description, case_numbers]
#    """
#    link = 'http://www.althingi.is/altext/xml/efnisflokkar/efnisflokkur/?efnisflokkur='
#    soup = soupUtils.getSoupFromLink(link + subject_id)
#
#    text = soup.find("heiti")
#
#    group_name = text[0]
#    subject_name = text[1]
#    subject_description = text[2]
#
#    return {
#        'id': subject_id,
#        'group_name': group_name,
#        'name': subject_name,
#        "description": subject_description,
#        "case_numbers": getCaseNumbers(soup)
#    }
#def getCaseNumbers(soup):
#    """
#    Takes in a soup and finds the 'málsnúmer' field
#    in the xml and returns a sorted list of them
#    """
#    case_numbers = soupUtils.get_attribute_value(soup, "mál", "málsnúmer")
#
    # Sort the case numbers
#    return case_numbers.sort()
