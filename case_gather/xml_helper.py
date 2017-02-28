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

def get_case_details(soup):
    """
    Function to retrieve case information from þingmál
    Interesting information:
        - Case status (if a law) (staðamáls)
        - Related case numbers (mál : málsnúmer)
        - subject id numbers (efnisflokkur : id)
    Output format [status, rel_casenumber, id_numbers]
    """
    status_gen = xml_helper.get_element_text(soup, "staðamáls")
    rel_cases_gen = xml_helper.get_attribute_value(soup, "mál", "málsnúmer")
    subj_id_gen = xml_helper.get_attribute_value(soup, "efnisflokkur", "id")

    output = []
    subj_ids = []
    rel_cases = []

    for rel_case in rel_cases_gen:
        rel_cases.append(rel_case)

    for subj_id in subj_id_gen:
        subj_ids.append(subj_id)

    status = next(status_gen)

    output = [status, rel_cases, subj_ids]
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
    goal_gen = xml_helper.get_element_text(soup, "markmið")
    changes_gen = xml_helper.get_element_text(soup, "helstuBreytingar")
    law_changes_gen = xml_helper.get_element_text(soup, "breytingaráLögum")
    costs_gen = xml_helper.get_element_text(soup, "kostnaðurOgTekjur")
    resolution_gen = xml_helper.get_element_text(soup, "afgreiðsla")

    goal = next(goal_gen)
    changes = next(changes_gen)
    law_changes = next(law_changes_gen)
    costs = next(costs_gen)
    resolution = next(resolution_gen)

    output = [goal, changes, law_changes, costs, resolution]
    return output