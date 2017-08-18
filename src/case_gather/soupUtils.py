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

    <element here=there >yes<element>
    Will return 'there' if 'element' and 'here' are the inputs
    """

    SOUP_LOGGER.info('looking for values: ' + element + "-" + attribute)
    values = []
    for value in soup.find_all(element):
        values.append(value[attribute])
    return values
