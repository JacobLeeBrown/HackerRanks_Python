import socket
import sys
from datetime import datetime


COMMON_WEB_PORTS = [21, 22, 23, 80, 110, 110, 111, 143, 443, 465, 587, 993, 995]


def _port_check(target_ip: str, target_port: int) -> int:
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = a_socket.connect_ex((target_ip, target_port))
    a_socket.close()
    return res


if __name__ == "__main__":

    remoteServer = input("Enter a remote host to scan: ")
    remoteServerIP = socket.gethostbyname(remoteServer)

    # Print a nice banner with information on which host we are about to scan
    print("-" * 60)
    print("Please wait, scanning remote host", remoteServerIP)
    print("-" * 60)

    f = open("port_scanner_output.txt", "r+")
    f.write("{} --- {} --- Open Ports\n".format(remoteServer, remoteServerIP))

    # Check what time the scan started
    t1 = datetime.now()

    try:
        # Check common ports first
        for port in COMMON_WEB_PORTS:
            result = _port_check(remoteServerIP, port)
            if result == 0:
                print("Port {}: Open".format(port))
                f.write(str(port) + '\n')

        # Check other ports from 1 to 1024
        for port in range(1, 1025):
            if port not in COMMON_WEB_PORTS:
                result = _port_check(remoteServerIP, port)
                if result == 0:
                    print("Port {}: Open".format(port))
                    f.write(str(port) + '\n')

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        f.close()
        sys.exit()

    except socket.gaierror:
        print("Hostname could not be resolved. Exiting")
        f.close()
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        f.close()
        sys.exit()

    # Close output file
    f.close()

    # Calculates the difference of time, to see how long it took to run the script
    t2 = datetime.now()
    total = t2 - t1

    # Printing the information to screen
    print("Scanning Completed in: ", total)
