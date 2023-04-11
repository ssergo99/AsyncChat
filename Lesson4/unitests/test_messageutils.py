"""

Unit-тесты отправки и получения сообщений

"""

import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))
from messageutils.get_send_message import send_msg, get_msg


class TestSock:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.enc_msg = None
        self.rcved_msg = None

    def send(self, mesg_to_send):
        json_test_msg = json.dumps(self.test_dict)
        self.enc_msg = json_test_msg.encode('utf-8')
        self.rcved_msg = mesg_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode('utf-8')


class Tests(unittest.TestCase):
    test_msg_to_send = {
        'action': 'presence',
        'time': 0.1,
        'user': {
            'account_name': 'Guest',
            'status': 'Ready for talk',
        }
    }
    test_msg_suc_stat = {"response": 200}
    test_msg_err_stat = {
        "response": 400,
        "error": "Bad Request"
    }

    def test_get_msg(self):
        test_sock_success = TestSock(self.test_msg_suc_stat)
        test_sock_error = TestSock(self.test_msg_err_stat)
        json_test_err_msg = json.dumps(self.test_msg_err_stat)
        test_err_msg = json_test_err_msg.encode('utf-8')
        json_test_suc_msg = json.dumps(self.test_msg_suc_stat)
        test_suc_msg = json_test_suc_msg.encode('utf-8')
        self.assertEqual(get_msg(test_sock_success), test_suc_msg)
        self.assertEqual(get_msg(test_sock_error), test_err_msg)

    def test_snd_msg(self):
        test_socket = TestSock(self.test_msg_to_send)
        send_msg(test_socket, self.test_msg_to_send)
        self.assertEqual(test_socket.enc_msg, test_socket.rcved_msg)


if __name__ == '__main__':
    unittest.main()
