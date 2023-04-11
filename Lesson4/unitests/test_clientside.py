"""

Unit-тесты для клиентской части кода

"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client_side import create_prs
from messageutils.check_message import serv_response_check


class TestClass(unittest.TestCase):

    def test_pres(self):
        test = create_prs()
        test['time'] = 0.1
        self.assertEqual(test, {'action': 'presence', 'time': 0.1, 'user': {'account_name': 'Anonymous',
                                                                            'status': 'Ready for talk'}})

    def test_success_resp(self):
        self.assertEqual(serv_response_check({'response': 200}), 'Success')

    def test_bad_req(self):
        self.assertEqual(serv_response_check({'response': 400, 'error': 'Bad Request'}), '400, error: Bad Request')

    def test_no_attr_resp(self):
        self.assertRaises(ValueError, serv_response_check, {'error': 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
