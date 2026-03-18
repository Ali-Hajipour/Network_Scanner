import argparse
import json
import sys
import os
from scanner import ful_scan , COMMON_SERVICE_PORTS
from reporter import print_summary , save_report

def parse_ports(port_string : str):


    if port_string.lower() == "common" :
        return list(COMMON_SERVICE_PORTS.keys())


    ports = set()


    for part in port_string.split(","):
        part = part.strip()
        if "-" in part:
            try :
                start , end = part.split("-" , 1)
                start ,end = int(start.strip()) , int(end.strip())
                if start > end or end >65535:
                    raise ValueError
                ports.update(range(start, end+1))
            except ValueError :
                print(f"Invalid Port : {part} must be in range of 1 to 65535")
                sys.exit(1)

    return sorted(ports)


