import unittest

import paramiko
from paramiko import SSHClient
from paramiko.ssh_exception import SSHException
from unittest.mock import MagicMock, patch

from main import SSH


class SSHTest(unittest.TestCase):

    def test_init_PASS(self):
        ssh_ = SSH()
        self.assertEqual(type(ssh_.client_), type(SSHClient()))

    @patch('main.SSH.connect_', MagicMock(return_value=SSHClient))
    def test_connect_PASS(self):
        ssh_ = SSH()
        ret_ = ssh_.connect_(hostname_='1.1.1.1',
                             port_=22,
                             username_='test',
                             password_='test')

        self.assertEqual(ret_, SSHClient)

    @patch('main.SSH.connect_', MagicMock(side_effect=SSHException))
    def test_connect_FAIL(self):

        ssh_ = SSH()

        with self.assertRaises(SSHException):
            ssh_.connect_(hostname_='1.1.1.1',
                          port_=22,
                          username_='test',
                          password_='test')

    @patch('main.SSH.connect_', MagicMock(return_value=True))
    @patch('paramiko.SSHClient.exec_command', MagicMock(return_value=0))
    def test_exec_command_PASS(self):

        ssh_ = SSH()
        ssh_.connect_(hostname_='1.1.1.1',
                      port_=22,
                      username_='test',
                      password_='test')

        re = ssh_.exec_command_(command_='test-command')
        print(re)


if __name__ == '__main__':
    unittest.main(verbosity=2)
