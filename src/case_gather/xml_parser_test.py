# pylint: disable=too-many-instance-attributes
import os
from django.test import TestCase
from django.conf import settings
from bs4 import BeautifulSoup

import case_gather.soupUtils as soupUtils
import case_gather.xml_parser as xml_parser
import case_gather.models as cgm
import parliament.models as parliament_models

case_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'caselist.xml')

details_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'casedetails.xml')

details3_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case3details.xml')

case_summary_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case_summary.xml')


class GetCaseSummary(TestCase):
    """
    Test get_case_summary in xml_parser.py
    """

    def setUp(self):
        with open(case_summary_path, 'rb') as f:
            case_summary_xml = f.read()
        self.case_summary_soup = BeautifulSoup(case_summary_xml, features='xml')

    def test_get_case_summary(self):
        goal, changes, law_changes, costs, resolution = xml_parser.get_case_summary(
            self.case_summary_soup
        )

        self.assertEqual(goal, 'Goals')
        self.assertEqual(changes, 'Changes')
        self.assertEqual(law_changes, 'Laws')
        self.assertEqual(costs, 'Costs')
        self.assertEqual(resolution, 'Resolution')
