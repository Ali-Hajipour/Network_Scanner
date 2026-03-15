import socket
import subprocess
import platform
import ipaddress
import concurrent.futures
import time
from subprocess import DEVNULL
from typing import List , Optional



COMMON_SERVICE_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    135:  "RPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    993:  "IMAPS",
    995:  "POP3S",
    1723: "PPTP",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}




def ping_host (ip : str , timeout : int =1 ) -> bool :

     os_select = "-n" if platform.system().lower() == "windows" else "-c"

     command = ["ping", os_select, "1" , "-W" , str(timeout) , str(ip)]

     try :
         result = subprocess.run(
             command,
             stdout=DEVNULL,
             stderr=DEVNULL,
             timeout = timeout +1

         )
         return result.returncode == 0

     except(subprocess.TimeoutExpired , FileNotFoundError) :
         return False



def find_hosts(network : str , max_workers : int = 50) -> List[str]:
    try :
        net = ipaddress.ip_network(network , strict=False)
    except ValueError  as e:
        raise ValueError(f"Inavlid network address {e}")

    hosts = [ ip(str) for ip in net.hosts() ]

    live_hosts = []

    print(f"/n scanning {len(hosts)} in {network}")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor :
        future_to_ip = {executor.submit(ping_host , ip): ip for ip in hosts}


        for future in concurrent.futures.as_completed (future_to_ip):

            ip = future_to_ip[future]


            try :
                if future.result(): live_hosts.append(ip); print("  [+] Host up: {ip}")

            except Exception :
                pass

                return sorted(live_hosts, key=lambda ip: ipaddress.ip_address(ip))
