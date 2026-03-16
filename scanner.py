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


def scan_port(ip : str ,port : int , timeout : float = 1.0 )-> Optional[str]:
    try:
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip , port))
        if result ==0 :
            banner = grab_banner(sock)
            sock.close()
            return banner if banner else ""

        else:
            sock.close()
            return None

    except (socket.error , socket.timeout , OSError):
        return None


def grab_banner(sock : socket.socket , size : int =1024) ->Optional[str]:
    try:
        sock.settimeout(1.5)
        banner = sock.recv(size)
        return banner.decode("utf-8" , errors="ignore").strip()
    except (socket.timeout , OSError):
        return None



def scan_host_ports (ip :str , ports : Optional[list[int]] = None , max_workers : int = 100 ,  timeout : float = 1.0 ) -> List[dict]:

    ports = list(COMMON_SERVICE_PORTS.keys()) if ports is None else ports
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, ip, port, timeout): port
            for port in ports
        }

        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                if result is not None :
                    open_ports.append({
                        "port" : port,
                        "ip" : ip,
                        "service" : COMMON_SERVICE_PORTS.get(port , "Unknown"),
                        "banner" : result[:100] if result else ""
                    })
            except Exception :
                pass

    return sorted(open_ports, key=lambda port: port["port"])

def ful_scan (
        target_ip : str ,
        ports :Optional[list[int]] = None ,
        port_workers : int =100 ,
        ping_workers : int =50,
        timeout : float = 1.0 ,
) -> dict :
    start_time = time.time()

    if "/" in target_ip :
        live_hosts = find_hosts(target_ip , max_workers = ping_workers)
    else :
        print(f"/n Scanning if ip : {target_ip} is available ... ")

        if ping_host(target_ip):
            print(f"  [+] {target_ip} is Available")
            live_hosts = [target_ip]
        else :
            print(f"  [!] {target_ip} May be Down (Scanning Anyway)")
            live_hosts = [target_ip]

    results = []


    for ip in live_hosts :

        open_ports = scan_host_ports(ip , ports , timeout = timeout )

        host_result = {
            "ip" : ip,
            "Status" : "Up",
            ports : open_ports,
            "Port Count" : len(open_ports)
        }

        try :
            hostname = socket.gethostbyaddr(ip)[0]
            host_result["Hostname"] = hostname
        except socket.herror :
            host_result["Hostname"] = "Unknown"

        results.append(host_result)

        if open_ports :
            print(f" {'PORT': < 8}  {'STATE' : < 8} {'Service' : <12} BANNER")
            print(f"'-' * 60")

            for p in open_ports:
                banner_preview = p["banner"][:40].replace("\n", " ") if p["banner"] else ""
                print(f"  {p['port']:<8} {p['state']:<8} {p['service']:<12} {banner_preview}")
            else :
                print(f"  [!] No open ports found in scanned range")
    time_consumed = time.time() - start_time

    return  {
        "target_ip" : target_ip,
        "Scan_time" : time_consumed,
        "Hosts Scanned Count" : len(live_hosts),
        "Up hosts Count" : len(results),
        "results" : results

    }






