"""

Unit-тесты для  серверной части кода

"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from messageutils.check_message import check_client_message


class TestServer(unittest.TestCase):
    errors_dic = {
        'response': 400,
        'error': 'Bad Request'
    }
    success_dic = {
        'response': 200
    }

    def test_succeess_req(self):
        self.assertEqual(check_client_message(
            {'action': 'presence', 'time': 0.1, 'user': {'account_name': 'Anonymous', 'status': 'Ready for talk'}}), self.success_dic)

    def test_no_user(self):
        self.assertEqual(check_client_message(
            {'action': 'presence', 'time': 0.1}), self.errors_dic)

    def test_no_action(self):
        self.assertEqual(check_client_message(
            {'time': '0.1', 'user': {'account_name': 'Anonymous', 'status': 'Ready for talk'}}), self.errors_dic)
    #
    def test_noprs_action(self):
        self.assertEqual(check_client_message(
            {'action': 'msg', 'time': 0.1, 'user': {'account_name': 'Anonymous', 'status': 'Ready for talk'}}), self.errors_dic)
    #
    def test_no_time(self):
        self.assertEqual(check_client_message(
            {'action': 'presence', 'user': {'account_name': 'Anonymous', 'status': 'Ready for talk'}}), self.errors_dic)

    def test_wrong_status(self):
        self.assertEqual(check_client_message(
            {'action': 'presence', 'time': 0.1, 'user': {'account_name': 'Anonymous', 'status': 'Do not disturb'}}), self.errors_dic)


if __name__ == '__main__':
    unittest.main()
