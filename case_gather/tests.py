from django.test import TestCase
from bs4 import BeautifulSoup
import os
from django.conf import settings

import case_gather.xml_helper as x_h
import case_gather.xml_parser as x_p
import case_gather.models as cgm

case_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'caselist.txt')

details_path = os.path.join(
    settings.BASE_DIR, 'case_gather', 'test_data', 'casedetails.txt')

# Create your tests here.


class XMLHelperGAVTestCase(TestCase):
    """
    Test GAV (get_attribute_value) from xml_helper.py
    """

    def setUp(self):

        with open(case_path, 'rb') as f:
            raw_xml = f.read()
        case_soup = BeautifulSoup(raw_xml, features='xml')

        cases = x_h.get_attribute_value(case_soup, 'mál', 'málsnúmer')
        self.case_number = next(cases)

        case_types_sh = x_h.get_attribute_value(
            case_soup, "málstegund", "málstegund")
        self.case_type_sh = next(case_types_sh)

    def test_case_number(self):
        self.assertEqual(self.case_number, '1')

    def test_case_types_sh(self):
        self.assertEqual(self.case_type_sh, 'l')


class XMLHelperGETTestCase(TestCase):
    """
    Test GET (get_element_text) from xml_helper.py
    """

    def setUp(self):
        with open(case_path, 'rb') as f:
            raw_xml = f.read()
        case_soup = BeautifulSoup(raw_xml, features='xml')

        case_names = x_h.get_element_text(case_soup, 'málsheiti')
        self.case_name = next(case_names)

        case_types = x_h.get_element_text(case_soup, 'heiti')
        self.case_type = next(case_types)

    def test_case_name(self):
        self.assertEqual(self.case_name, 'fjárlög 2017')

    def test_case_type(self):
        self.assertEqual(self.case_type, 'Frumvarp til laga')


class XMLHelperGCDTestCase(TestCase):
    """
    Test get_case_details in xml_helper
    """

    def setUp(self):
        with open(details_path, 'rb') as f:
            details_xml = f.read()

        details_soup = BeautifulSoup(details_xml, features='xml')

        status_gen = x_h.get_element_text(details_soup, 'staðamáls')
        rel_cases_gen = x_h.get_attribute_value(
            details_soup, 'mál', 'málsnúmer')
        # rel_cases_gen = x_h.get_attribute_value(
        #     details_soup, 'þingskjal', 'málsnúmer')
        subj_id_gen = x_h.get_attribute_value(
            details_soup, 'efnisflokkur', 'id')

        self.output = x_h.get_case_details(details_soup)

        self.status = next(status_gen)

        rel_cases = []
        subj_ids = []
        for rel_case in rel_cases_gen:
            rel_cases.append(rel_case)
        for subj_id in subj_id_gen:
            subj_ids.append(subj_id)

        rel_cases.pop(0)
        self.rel_cases = rel_cases
        self.subj_ids = subj_ids

    def test_status(self):
        self.assertEqual(self.status, 'Samþykkt sem lög frá Alþingi.')

    def test_related_cases(self):
        self.assertEqual(self.rel_cases, ['2', '2'])

    def test_subj_id(self):
        self.assertEqual(self.subj_ids, ['6'])

    def test_get_gase_details(self):
        status, rel_cases, subj_ids = self.output
        self.assertEqual(status, 'Samþykkt sem lög frá Alþingi.')
        self.assertEqual(rel_cases, ['2', "2"])
        self.assertEqual(subj_ids, ['6'])


class XMLParserCaseCollectorTestCase(TestCase):
    """
    Test case_collector function in xml_parser.py
    """

    def setUp(self):
        gen = x_p.case_collector(146)
        self.number, self.name, self.case_type = next(gen)

    def test_case_collector_number(self):
        self.assertEqual(self.number, '1')

    def test_case_collector_name(self):
        self.assertEqual(self.name, 'fjárlög 2017')

    def test_case_collector_type(self):
        self.assertEqual(self.case_type, 'l')


class XMLParserGetCases(TestCase):
    """
    Test function get_cases in xml_parser.py
    """

    def setUp(self):
        case_gen = x_p.get_cases(146)

        self.case = next(case_gen)
        self.number = self.case[0]
        self.name = self.case[1]
        self.case_type = self.case[2]

    def test_number(self):
        self.assertEqual(self.number, '1')

    def test_name(self):
        self.assertEqual(self.name, 'fjárlög 2017')

    def test_case_type(self):
        self.assertEqual(self.case_type, 'l')


class XMLParserGetCaseData(TestCase):
    """
    Test function get_case_data in xml_parser.py
    """

    def setUp(self):
        case_data_gen = x_p.get_case_data(146)

        self.case_data = next(case_data_gen)
        self.number = self.case_data['number']
        self.name = self.case_data['name']
        self.rel_cases = self.case_data['rel_cases']
        self.case_type = self.case_data['case_type']
        self.session = self.case_data['session']
        self.case_status = self.case_data['case_status']
        self.subjects = self.case_data['subjects']

    def test_number(self):
        self.assertEqual(self.number, '1')

    def test_name(self):
        self.assertEqual(self.name, 'fjárlög 2017')

    def test_rel_cases(self):
        self.assertEqual(self.rel_cases, ['2', '2'])

    def test_case_type(self):
        self.assertEqual(self.case_type, 'l')

    def test_session(self):
        self.assertEqual(self.session, 146)

    def test_case_status(self):
        self.assertEqual(self.case_status, 'Samþykkt sem lög frá Alþingi.')

    def test_subjects(self):
        self.assertEqual(self.subjects, ['6'])


class ServicesTestCase(TestCase):
    """
    Test services.py functionality
    """

    def setUp(self):
        case_data_gen = x_p.get_case_data(146)

        self.case_data = next(case_data_gen)

    def test_object_creation(self):
        cgm.Case.objects.create(name=self.case_data['name'],
                                number=int(self.case_data['number']),
                                parliament_session=int(self.case_data['session']),
                                case_type=self.case_data['case_type'],
                                case_status=self.case_data['case_status'])

        number = cgm.Case.objects.filter(number=1)
        self.assertEqual(number, 1)
