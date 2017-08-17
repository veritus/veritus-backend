import os

from django.test import TestCase
from django.conf import settings
from bs4 import BeautifulSoup

import case_gather.soupUtils as soupUtils

case_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'caselist.xml')


class GetAttributeValue(TestCase):
    """
    Test get_attribute_value from soupUtils.py
    """

    def setUp(self):

        with open(case_path, 'rb') as f:
            raw_xml = f.read()
        self.case_soup = BeautifulSoup(raw_xml, features='xml')

    def test_case_number(self):
        cases = soupUtils.get_attribute_value(self.case_soup, 'mál', 'málsnúmer')
        case_number = next(cases)
        self.assertEqual(case_number, '1')
        case_number = next(cases)
        self.assertEqual(case_number, '2')
        case_number = next(cases)
        self.assertEqual(case_number, '3')


class GetElementText(TestCase):
    """
    Test get_element_text from soupUtils.py
    """

    def setUp(self):
        with open(case_path, 'rb') as f:
            raw_xml = f.read()
        self.case_soup = BeautifulSoup(raw_xml, features='xml')

    def test_case_name(self):
        case_names = soupUtils.get_element_text(self.case_soup, 'málsheiti')
        case_name = next(case_names)
        self.assertEqual(case_name, 'fjárlög 2017')
        case_name = next(case_names)
        self.assertEqual(case_name, 'ýmsar forsendur fjárlagafrumvarps 2017')
        case_name = next(case_names)
        self.assertEqual(case_name, 'sálfræðiþjónusta í framhaldsskólum')
