import os

from django.test import TestCase
from django.conf import settings
from bs4 import BeautifulSoup

import case_gather.soupUtils as soupUtils

case_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case_list.xml')


class GetAttributeValue(TestCase):
    """
    Test get_attribute_value from soupUtils.py
    """

    def setUp(self):

        with open(case_path, 'rb') as f:
            raw_xml = f.read()
        self.case_soup = BeautifulSoup(raw_xml, features='xml')

    def test_case_number(self):
        cases = soupUtils.get_attribute_value(
            self.case_soup, 'mál', 'málsnúmer')
        self.assertEqual(cases, ['1', '2', '3'])
