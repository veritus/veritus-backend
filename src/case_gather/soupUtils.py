import logging
import requests

from bs4 import BeautifulSoup

SOUP_LOGGER = logging.getLogger('soupUtils')

def getSoupFromLink(link):
    """
    Takes in a URL link that returns XML
    and returns a BeautifulSoup object
    """
    return BeautifulSoup(requests.get(link).content, features="xml")

def get_attribute_value(soup, element, attribute):
    """
    element: name of element as a str
    attribute: name of element attribute as a str
    yield attribute values as is (can be strings or ints, beware!)

    Interesting elements : attribute pairs:
        - mál : málsnúmer
    """

    SOUP_LOGGER.info('looking for values: ' + element +"-" + attribute)
    d = {element: attribute}
    values = soup.findAll(d)
    for value in values:
        yield value[attribute]


def get_element_text(soup, element_name):
    """
    element: name of element as a str
    yield element text as is

    interesting elements:
        - málsheiti
        - heiti
        - heiti2
        - xml
    """

    SOUP_LOGGER.info('looking for elements: ' + element_name)
    elements = soup.findAll(element_name)
    for element in elements:
        yield element.text
