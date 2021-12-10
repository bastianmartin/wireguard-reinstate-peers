import subprocess
import datetime
import socket


def valid_ip(address):
    try:
        if ':' in address:
            socket.inet_aton(address.split(':')[0])
        else:
            socket.inet_aton(address)
        return True
    except socket.error:
        return False


class ReinstateWgPeers:
    wg_if = "wg0"
    remove_command = "wg set %s peer %s remove"
    reinstate_command = "wg set %s peer %s allowed-ips %s"

    def __init__(self):
        try:
            result = subprocess.check_output("wg show wg0 dump", shell=True)
        except BaseException:
            print('There does not seem to be a valid output from the wg show dump command!')
            exit()

        lines = result.decode().splitlines()

        for i in range(0, len(lines)):
            line = lines[i].strip().split('\t')

            if len(line) == 8:
                if int(line[4]) > 0:
                    delta = int(datetime.datetime.now().timestamp()) - int(line[4])

                    # if delta is > 180 (seconds) then remove peer and reinstate it again
                    if delta > 180:
                        remove_command = self.remove_command % (self.wg_if, line[0])
                        reinstate_command = self.reinstate_command % (self.wg_if, line[0], line[3])
                        subprocess.run(remove_command.split())
                        subprocess.run(reinstate_command.split())
                else:
                    if valid_ip(line[2]):
                        remove_command = self.remove_command % (self.wg_if, line[0])
                        reinstate_command = self.reinstate_command % (self.wg_if, line[0], line[3])
                        subprocess.run(remove_command.split())
                        subprocess.run(reinstate_command.split())


B = ReinstateWgPeers()
