import logging


def get_attribute_value(soup, element, attribute):
    """ 
    element: name of element as a str
    attribute: name of element attribute as a str
    yield attribute values as is (can be strings or ints, beware!)

    Interesting elements : attribute pairs:
        - mál : málsnúmer
    """
    logger = logging.getLogger('xmlHelper')

    logger.info('looking for values')
    d = {element: attribute}
    try:
        values = soup.findAll(d)
        logger.info('have values')
        for value in values:
            logger.info('yielding value: ' + value[attribute])
            yield value[attribute]
    except Exception as e:
        logger.error(e.message)


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
    logger = logging.getLogger('xmlHelper')

    logger.info('looking for elements')
    try:
        elements = soup.findAll(element)
        logger.info('have elements')
        try:
            for element in elements:
                logger.info('yielding element: ' + element.text)
                yield element.text
        except Exception as e:
            logger.error(e)
    except Exception as e:
        logger.error(e.message)


def get_case_details(soup):
    """
    Function to retrieve case information from þingmál
    Interesting information:
        - Case status (if a law) (staðamáls)
        - Related case numbers (mál : málsnúmer)
        - subject id numbers (efnisflokkur : id)
    Output format [status, rel_casenumber, id_numbers]
    """
    logger = logging.getLogger('xmlHelper')
    logger.info('starting get_case_details')

    status_flag = True
    try:
        status_gen_ = get_element_text(soup, "staðamáls")
        test = next(status_gen_)
        assert test is not None
        status_flag = True
        status_gen = get_element_text(soup, 'staðamáls')
    except:
        logger.info('Case has no status')
        status_flag = False

    rel_cases_gen = get_attribute_value(soup, "mál", "málsnúmer")
    subj_id_gen = get_attribute_value(soup, "efnisflokkur", "id")

    output = []
    subj_ids = []
    rel_cases = []
    logger.info('Adding related cases to list')
    for rel_case in rel_cases_gen:
        rel_cases.append(rel_case)

    # remove the first rel_case, as it is the actual case
    rel_cases.pop(0)

    logger.info('adding subject ids to list')
    for subj_id in subj_id_gen:
        subj_ids.append(subj_id)

    if status_flag:
        logger.info('creating case status generator')
        status = next(status_gen)
    else:
        status = ''

    output = [status, rel_cases, subj_ids]
    logger.info('returning case details output')
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
    logger = logging.getLogger('xmlHelper')
    logger.info('starting get_case_summary')

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

    output = [goal, changes, law_changes, costs, resolution]
    return output
