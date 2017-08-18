# pylint: disable=too-many-instance-attributes
import os
from django.test import TestCase
from django.conf import settings
from bs4 import BeautifulSoup

import case_gather.soupUtils as soupUtils
import case_gather.xml_parser as xml_parser
import case_gather.models as cgm
import parliament.models as parliament_models

case_creators_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case_creators.xml')

class GetCaseCreatorNames(TestCase):
    """
    Test getCaseCreatorNames in xml_parser.py
    """

    def setUp(self):
        with open(case_creators_path, 'rb') as f:
            case_creators_xml = f.read()
        self.case_creators_soup = BeautifulSoup(case_creators_xml, features='xml')

    def test_get_case_creators(self):
        case_creators = xml_parser.getCaseCreatorNames(
            self.case_creators_soup
        )
        expected = ['John', 'James', 'Jonathan']

        self.assertEqual(expected, case_creators)

related_cases_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case_list.xml')

class GetRelatedCases(TestCase):
    """
    Test getRelatedCases in xml_parser.py
    """

    def setUp(self):
        with open(related_cases_path, 'rb') as f:
            related_cases_xml = f.read()
        self.related_cases_soup = BeautifulSoup(related_cases_xml, features='xml')

    def test_get_case_creators(self):
        related_cases = xml_parser.getRelatedCases(
            self.related_cases_soup
        )
        expected = ['2', '3']

        self.assertEqual(expected, related_cases)

subject_names_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'subject_names.xml')

class GetSubjectNames(TestCase):
    """
    Test getSubjectNames in xml_parser.py
    """

    def setUp(self):
        with open(subject_names_path, 'rb') as f:
            subject_names_xml = f.read()
        self.subject_names_soup = BeautifulSoup(subject_names_xml, features='xml')

    def test_get_case_creators(self):
        subject_names = xml_parser.getSubjectNames(
            self.subject_names_soup
        )
        expected = [
            'Alþjóðasamningar og utanríkismál',
            'Löggæsla og eftirlit'
        ]

        self.assertEqual(expected, subject_names)


status_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'status.xml')

class GetStatus(TestCase):
    """
    Test getStatus in xml_parser.py
    """

    def setUp(self):
        with open(status_path, 'rb') as f:
            status_xml = f.read()
        self.status_soup = BeautifulSoup(status_xml, features='xml')

    def test_get_case_creators(self):
        status = xml_parser.getStatus(
            self.status_soup
        )
        expected = 'Samþykkt sem lög frá Alþingi.'

        self.assertEqual(expected, status)

cases_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'case_list.xml')

class CollectCases(TestCase):
    """
    Test collectCases in xml_parser.py
    """

    def setUp(self):
        with open(cases_path, 'rb') as f:
            cases_xml = f.read()
        self.cases_soup = BeautifulSoup(cases_xml, features='xml')

    def test_get_case_creators(self):
        cases = xml_parser.collectCases(
            self.cases_soup
        )
        expected_case_one = {
            "number": "1",
            'name': "fjárlög 2017",
            'case_type': "Frumvarp til laga",
            'althingi_link': "http://www.althingi.is/dba-bin/ferill.pl?ltg=146mnr=1"
        }
        expected_case_two = {
            "number": "2",
            'name': "ýmsar forsendur fjárlagafrumvarps 2017",
            'case_type': "Frumvarp til laga",
            'althingi_link': "http://www.althingi.is/dba-bin/ferill.pl?ltg=146mnr=2"
        }
        expected_case_three = {
            "number": "3",
            'name': "sálfræðiþjónusta í framhaldsskólum",
            'case_type': "Tillaga til þingsályktunar",
            'althingi_link': "http://www.althingi.is/dba-bin/ferill.pl?ltg=146mnr=3"
        }

        self.assertEqual(cases[0], expected_case_one)
        self.assertEqual(cases[1], expected_case_two)
        self.assertEqual(cases[2], expected_case_three)
