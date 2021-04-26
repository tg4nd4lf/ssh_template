import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException


class SSH:

    def __init__(self):
        self.client_ = paramiko.SSHClient()
        self.client_.load_system_host_keys()
        self.client_.set_missing_host_key_policy(paramiko.WarningPolicy)

    def connect_(self):

        try:
            self.client_.connect(hostname='192.168.178.63',
                                 port=22,
                                 username='userjw',
                                 password='1q2w3e4r')

            print("Connect to client ...")
            return self

        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")

        except BadHostKeyException as err:
            print("Unable to verify server's host key: %s" % err)

        except SSHException as err:
            print("Unable to establish SSH connection: %s" % err)

    def exec_command_(self, command_: str):

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

    def disconnect_(self):

        try:
            self.client_.close()
            print("Connection closed.")

        except SSHException as err:
            print("Unable to close connection: %s" % err)


if __name__ == "__main__":
    ssh_client_ = SSH()

    ssh_client_.connect_()

    response_ = ssh_client_.exec_command_('hostname -I')
    print(response_)

    ssh_client_.disconnect_()

