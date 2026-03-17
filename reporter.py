import json
import os
from datetime import datetime
from typing import Dict

def print_summary(scan_results : Dict) -> None:

    results = scan_results.get("results" , [])
    target = scan_results.get("target" , "")
    time_consumed = scan_results.get("time_consumed" , 0)
    hosts_up = scan_results.get("hosts_up", 0)
    total = scan_results.get("total" , 0)

    print("\n" + "=" *60)
    print("SCAN IS COMPLETED")
    print("=" *60)
    print(f"target : {target}" )
    print(f"Hosts scanned : {total}" )
    print(f"Hosts Up : {hosts_up}" )
    print(f"Time Consumed : {time_consumed}" )
    print("=" *60)

    if not results:
        print("\n No Live Hosts Found. \n")
        return


    for hosts in results:
        ip = hosts["ip"]
        hostname= hosts.get("hostname" , "")
        open_ports = hosts.get("open_ports" , [])

