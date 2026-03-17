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

    # Overall overview of Scanned Hosts
    print("\n" + "=" *60)
    print("SCAN IS COMPLETED")
    print("=" *60)
    print(f"target : {target}" )
    print(f"Hosts scanned : {total}" )
    print(f"Hosts Up : {hosts_up}" )
    print(f"Time Consumed : {time_consumed}" )
    print("=" *60)

    if not results: # if no hosts are found.
        print("\n No Live Hosts Found. \n")
        return


    for host in results: # Information about each specific alive host.
        ip = host["ip"]
        hostname= host.get("hostname" , "")
        open_ports = host.get("open_ports" , [])


        label = f"{ip}"

        if hostname : #it adds the hostname to the label if the host name is available
            label += f" ({hostname})"

        print(f"Host : {label}")
        print(f"Open Port(s) : {host['open_ports']}")


        if open_ports: #printing open ports
            print(f"\n {'PORT' :< 8} {'SERVICE' : < 14} BANNER ")
            print(f"{'-' * 60}")
            for port in open_ports: # g
                banner = port.get("banner" , "").split()[0][:40]
                print(f"{port['port']:< 8} {port['service'] : < 14} {banner}")
            else:
                print("No open ports detected.")
            print(f"{'='*60}")


def save_report(scan_results : Dict ,  file_path : str) -> None:
    output = {
        #General data about the scan
        "scan_metadata" : {
            "tool" : "Network Scanner (Created by Ali Hajipour)",
            "phase" : 1,
            "timestamp" : datetime.utcnow().isoformat()+ "UTC",
            "target" : scan_results.get("target" + ""),
            "scan_time" : scan_results.get("time_consumed" , 0),
            "hosts_scanned" : scan_results.get("hosts_scanned" , 0),
            "hosts_up" : scan_results.get("hosts_up" , 0)
        },
        #Specific information about the scan.
        "hosts" : scan_results.get("hosts" , []),
    }

    try: # writing the results on a file
        with open( file_path , "w" ,encoding = "utf-8" ) as f:
            json.dump(output , f , indent = 2)
            print(f"Results Saved to {os.path.abspath(file_path)} Successfully !")
    except OSError as e:
        print(f"Unfortunately, Results Failed to Save : {e}")


def load_report(file_path :  str ) -> Dict:
    with open(file_path , "r", encoding = "utf-8" ) as f:
        return json.load(f)