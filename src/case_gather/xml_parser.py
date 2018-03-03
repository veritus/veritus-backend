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
    print('before soup')
    cases_soup = soupUtils.getSoupFromLink(link + str(parliament_session_number))
    print('after soup')
    cases = collectCases(cases_soup)

    link_details = """http://www.althingi.is/altext/xml/thingmalalisti/thingmal/?lthing=%i&malnr=""" % parliament_session_number
    cases_data = []
    for case in cases:
        # Go through cases and get more details from them
        try:
            print('lookin at '+case['number'])
            details_soup = soupUtils.getSoupFromLink(link_details + str(case['number']))
            print('after soup lookin at')
            case = {
                'number': case['number'],
                'name': case['name'],
                'rel_cases': getRelatedCases(details_soup),
                'case_type': case['case_type'],
                'session': parliament_session_number,
                'althingi_status': getStatus(details_soup),
                'subject_names': getSubjectNames(details_soup),
                'althingi_link': case['althingi_link'],
                'case_creator_names': getCaseCreatorNames(details_soup)
            }
            print(case['name'])
            cases_data.append(case)
        except:
            print('error')
    print(cases_data)
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
    status = soup.find("staðamáls")
    print(status)
    if status:
        return status.string
    return ""


def getSubjectNames(soup):
    """
        Takes in a soup, finds all subjects and returns
        a list of their names
    """
    subject_names = []
    for subject_element in soup.find_all('efnisflokkur'):
        subject_name = subject_element.find("heiti").string
        subject_names.append(subject_name)
    print('subjectnames')
    print(subject_names)
    return subject_names

def getRelatedCases(soup):
    """
        Takes in a soup and finds all relevant cases and returns
        their ids
    """
    related_cases = soupUtils.get_attribute_value(soup, "mál", "málsnúmer")
    print('related_cases')
    print(related_cases)
    # remove the first rel_case, as it is the actual case
    if related_cases:
        related_cases.pop(0)
    return related_cases

def getCaseCreatorNames(soup):
    """
        Takes in a soup and finds the 'framsögumaður'
        goes through them all, adds their names to a list
        and returns said list
    """
    case_creators_elements = soup.find_all("framsögumaður")
    case_creators_names = []
    for case_creator_element in case_creators_elements:
        name = case_creator_element.find('nafn').string
        case_creators_names.append(name)
    print('casecreatornames')
    print(case_creators_names)
    return case_creators_names
