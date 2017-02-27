#!/usr/bin/python


def get_attribute_value(soup, element, attribute):
    """ 
    element: name of element as a str
    attribute: name of element attribute as a str
    yield attribute values as is (can be strings or ints, beware!)

    Interesting elements : attribute pairs:
        - mál : málsnúmer
    """
    d = {element: attribute}
    values = soup.findAll(d)

    for value in values:
        yield value[attribute]


def get_element_text(soup, element):
    """
    element: name of element as a str
    yield element text as is

    interesting elements:
        - málsheiti
        - heiti
        - heiti2 
        - xml
    """
    elements = soup.findAll(element)

    for element in elements:
        yield element.text


def get_subject(subject_id):
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
    link = "http://www.althingi.is/altext/xml/efnisflokkar/\
        efnisflokkur/?efnisflokkur="
    soup = get_xml(link + subject_id)

    d = {}

    try:
        group_number = get_attribute_value(soup, "yfirflokkur", "id")
        assert group_number is None
    except:
        # log group_id
        pass
    else:
        text = get_element_text(soup, "heiti")

        group_name = next(text)
        subject_name = next(text)
        subject_description = next(text)

        cases = get_attribute_value(soup, "mál", "málsnúmer")

        # Build list of case numbers
        case_numbers = []
        for number in cases:
            case_numbers.append(number)

        # Sort the case numbers
        case_numbers.sort()
        d = {'id': subject_id,
             'group_name': group_name,
             'name': subject_name,
             "description": subject_description,
             "case_numbers": case_numbers}
    finally:
        group_number.close()
        text.close()
        cases.close()
        return d


def get_subjects():
    """
    Function to yield from get_subjects
    Format of output is [subject_id, group_name, subject_name,
                                        subject_description, case_numbers]
            """
    for i in range(1, 100):
        d = get_subject(i)
        if d is not None:
            yield d
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
    link = "http://www.althingi.is/altext/xml/thingmalalisti/?lthing="
    soup = get_xml(link + str(parliament_session_number))

    case_numbers_gen = get_attribute_value(soup, "mál", "málsnúmer")
    case_names_gen = get_element_text(soup, "heiti")
    case_types_gen = get_attribute_value(soup, "málstegund", "málstegund")

    d = []
    try:
        while True:
            number = next(case_numbers_gen)
            name = next(case_names_gen)
            case_type = next(case_types_gen)

            assert number is not None
            d = [number, name, case_type]
            yield d
    except:
        # log that cases have been iterated over
        pass
    finally:
        case_numbers_gen.close()
        case_names_gen.close()
        case_types_gen.close()


def get_case_details(soup):
    """
    Function to retrieve case information from þingmál
    Interesting information:
        - Case status (if a law) (staðamáls)
        - Related case numbers (mál : málsnúmer)
        - subject id numbers (efnisflokkur : id)
    Output format [status, rel_casenumber, id_numbers]
    """
    status_gen = get_element_text(soup, "staðamáls")
    rel_cases_gen = get_attribute_value(soup, "mál", "málsnúmer")
    subj_id_gen = get_attribute_value(soup, "efnisflokkur", "id")

    d = []
    subj_ids = []
    rel_cases = []

    for rel_case in rel_cases_gen:
        rel_cases.append(rel_case)

    for subj_id in subj_id_gen:
        subj_ids.append(subj_id)

    status = next(status_gen)

    d = [status, rel_cases, subj_ids]
    return d


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
    goal_gen = get_element_text(soup, "markmið")
    changes_gen = get_element_text(soup, "helstuBreytingar")
    law_changes_gen = get_element_text(soup, "breytingaráLögum")
    costs_gen = get_element_text(soup, "kostnaðurOgTekjur")
    resolution_gen = get_element_text(soup, "afgreiðsla")

    goal = next(goal_gen)
    changes = next(changes_gen)
    law_changes = next(law_changes_gen)
    costs = next(costs_gen)
    resolution = next(resolution_gen)

    d = [goal, changes, law_changes, costs, resolution]
    return d


def get_case_data(parliament_session_number):
    """
    Combines get_case_details and get_case_summary into a list
    that will suffice to create a Case object for database
    summary : [goal, changes, law_changes, costs, resolution]
    details : [status, rel_cases, subj_ids]
    output has keys: 'number', 'name', 'case_type', 'case_status', 'rel_cases'
                                'subjects', 'sessions'
    """
    # link_summary = "http://www.althingi.is/altext/xml/samantektir\
    #     /samantekt/?lthing=146&malnr="
    link_details = "http://www.althingi.is/altext/xml/\
        thingmalalisti/thingmal/?lthing=146&malnr="

    case = get_cases(parliament_session_number)

    # used keys at this point:
    # number, session, name, case_type, case_status, rel_cases, subjects
    # more can be added as models are changed or added
    d = {}

    for number, name, case_type in case:
        # summary_soup = get_xml(link_summary + str(number))
        details_soup = get_xml(link_details + str(number))

        details = get_case_details(details_soup)
        # summary = get_case_summary(summary_soup)

        case_status = details[0]
        rel_cases = details[1]
        subjects = details[2]

        d = {'number': number, 'name': name,
             'case_type': case_type, 'case_status': case_status,
             'rel_cases': rel_cases, 'subjects': subjects,
             'session': parliament_session_number}

        yield d


def get_xml(link):
    import requests
    from bs4 import BeautifulSoup

    try:
        result = requests.get(link)
    except Exception as e:
        print("Error performing request:", e)
    else:
        content = result.content
        soup = BeautifulSoup(content, features="xml")
        return soup
    finally:
        pass


def main():
    sess_number = 146
    get_case_details(sess_number)


if __name__ == '__main__':
    main()
