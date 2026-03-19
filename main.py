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

def main():
    parser = argparse.ArgumentParser(
        prog="Network scanner",
        description= "Network Scanner — host discovery + TCP port scanning",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="""
        Examples:
          python main.py 192.168.1.1
          python main.py 192.168.1.0/24 -p 1-1024
          python main.py 10.0.0.1 -p 22,80,443 -o report.json
          python main.py 192.168.1.0/24 --threads 200 --timeout 0.5
         
        Legal notice: Only scan networks you own or have written permission to scan.
        """
    )

    parser.add_argument(
        "target",
        help = "Target IP Address (192.168.1.1) or Subnet in CIDR format (192.168.1.0/24)")

    parser.add_argument(
        "-p" , "--port",
        default = "common",
        metavar = "COMMON_SERVICE_PORT",
        help= "Ports to scan: 'common', '80', '22,80,443', '1-1024' (default: common)"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=100,
        metavar="N",
        help="Number of concurrent threads for port scanning (default: 100)"
    )

    parser.add_argument(
        "--ping-threads",
        type = int,
        default = 50,
        metavar = "N",
        help="Threads for ping sweep / host discovery (default: 50)"

    )


    parser.add_argument(
        "--timeout",
        type = float,
        default = 1.0,
        metavar = "SECS",
        help = "TCO Connection Timeout per port in seconds (default: 0.5)"
    )

    parser.add_argument(
        "-o" , "--output",
        metavar = "FILE",
        help = "Save results as JSON to this file (e.g. results.json)"
    )

    args = parser.parse_args()

    ports = parse_ports(args.port)



    print("=" * 60)
    print("  Network Scanner v1.0  —  Phase 1 (Core)")
    print("=" * 60)
    print(f"  Target  : {args.target}")
    print(f"  Ports   : {len(ports)} port(s) selected")
    print(f"  Threads : {args.threads} (port) / {args.ping_threads} (ping)")
    print(f"  Timeout : {args.timeout}s per port")
    print("=" * 60)


    try:
        result = ful_scan(args.target ,
                          ports, port_workers=args.threads ,
                          ping_workers=args.ping_threads ,
                          timeout=args.timeout
        )
    except ValueError as e :
        print(f" An error has occurred: {e}")
        sys.exit(1)
    except KeyboardInterrupt as e :
        print(f" The process was interrupted by User : {e}")
        sys.exit(0)

    print_summary(result)

    if args.output:
        save_report(result, args.output)
    return 0
if __name__ == "__main__":
    sys.exit(main())