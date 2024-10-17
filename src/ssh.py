#!/usr/bin/env python3

# Filename: main.py

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


""" SSH Class"""

import paramiko

from typing import  Any
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

__author__ = "tg4nd4lf"
__version__ = "1.0"


class SSH:
    """
    # Example
    import os
    from dotenv import load_dotenv
    load_dotenv('../.env')  # Load the environment variables from the .env file

    ssh_client_ = SSH()

    ssh_client_.connect_(hostname_=os.getenv('HOSTNAME'),
                         username_=os.getenv('USERNAME'),
                         password_=os.getenv('PASSWORD'))

    response_ = ssh_client_.exec_command_('pwd')
    print(response_)

    ssh_client_.disconnect_()
    """

    def __init__(self):
        self.client_ = paramiko.SSHClient()
        self.client_.load_system_host_keys()
        self.client_.set_missing_host_key_policy(paramiko.WarningPolicy)

    def __repr__(self):
        return f'SSH: {self.client_}'

    def connect_(self, hostname_: str = None, port_: int = 22, username_: str = None, password_: str = None) -> paramiko.SSHClient.connect:
        """
        Connect to hostname.

        :param hostname_: Hostname/IP of device.
        :param port_: Port of device. Default: 22.
        :param username_: Username.
        :param password_: String.
        :return:
        """

        try:
            self.client_.connect(hostname=hostname_,
                                 port=port_,
                                 username=username_,
                                 password=password_)

            print("Connect to client ...")
            return self

        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")

        except BadHostKeyException as err:
            print("Unable to verify server's host key: %s" % err)

        except SSHException as err:
            print("Unable to establish SSH connection: %s" % err)

    def exec_command_(self, command_: str) -> list[str | bytes | Any]:
        """
        Execute command with connection before.

        :param command_: Command as string to be executed.
        :return:
        """

        try:
            _, stdout, stderr = self.client_.exec_command(command=command_)

            if stdout.channel.exit_status_ready():
                if stdout.channel.recv_exit_status() == 0:
                    return stdout.readlines()

                else:
                    return stderr.readlines()

            else:
                while not stdout.channel.exit_status_ready():
                    if stdout.channel.recv_ready():
                        if stdout.channel.recv_exit_status() == 0:
                            return stdout.readlines()

        except TimeoutError as err:
            print("Unable to execute command: %s" % err)

        except SSHException as err:
            print("Unable to execute command: %s" % err)

    def disconnect_(self) -> bool:
        """
        Disconnect from device.

        :return: True: Success. False: Failure.
        """

        try:
            self.client_.close()
            print("Connection closed.")
            return True

        except SSHException as err:
            print("Unable to close connection: %s" % err)
            return False


if __name__ == "__main__":
    pass
