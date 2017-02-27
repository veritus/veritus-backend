from django.test import TestCase
from bill_gather.xml_parser import get_case_data

# Create your tests here.

# class ModelsTestCase(TestCase):
    # def setUp(self):
    #     new_cases = get_case_data(146)
    #     case = next(new_cases)
    #     new_cases.close()
    #     # output has keys: 'number', 'name', 'case_type', 'case_status', 'rel_cases'
    #     #                             'subjects', 'sessions'
    #     self.case

    # def testNumber(self):
    #     case = self.case
    #     assertEqual(int(case['number']), 1)

    # def testName(self):
    #     case = self.case
    #     assertEqual(case['name'], "fjárlög 2017")

    # def testType(self):
    #     assertEqual(self.case['case_type'], "l")

    # def testStatus(self):
    #     assertEqual(self.case['case_status'], "Samþykkt sem lög frá Alþingi.")

    # def testSubjects(self):
    #     assertEqual(self.case['subjects'], ['6'])

    # def testSessions(self):
    #     assertEqual(self.case['sessions'], 146)





