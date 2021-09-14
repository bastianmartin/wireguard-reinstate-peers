import subprocess
import datetime


def process():
    result = subprocess.check_output("wg show wg0 dump", shell=True)
    lines = result.decode().splitlines()

    for i in range(0, len(lines)):
        line = lines[i].strip().split('\t')

        if len(line) == 8:
            if int(line[4]) > 0:
                delta = int(datetime.datetime.now().timestamp()) - int(line[4])

                # if delta is > 180 (seconds) then remove peer and reinstate it again
                if delta > 180:
                    remove_command = "wg set wg0 peer %s remove" % line[0]
                    reinstate_command = "wg set wg0 peer %s allowed-ips %s" % (line[0], line[3])

                    # remove outdated peer
                    subprocess.run(remove_command.split())
                    subprocess.run(reinstate_command.split())


process()
