import os.path
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from scanner import ful_scan , COMMON_SERVICE_PORTS

sys.path.insert(0 , os.path.dirname(os.path.abspath(__file__)))


app = FastAPI(
    title = "Advanced Network Scanner",
    description="Developed by Ali Hajipour",
    version="1.0",
)

app.mount("/static", StaticFiles(directory="web"), name="static")

class ScanRequest(BaseModel):
    target : str
    ports : Optional[str] = "common"
    threads : Optional[int] = 100
    ping_threads : Optional[int] = 50
    timeout : Optional[float] = 1.0

class PortResult(BaseModel):
    port : int
    state : str
    service : str
    banner : str

class HostResult(BaseModel):
    ip : str
    hostname : str
    status : str
    port_count : int
    open_ports : List[PortResult]

class scanResponse(BaseModel):
    target : str
    scan_time : float
    hosts_scanned : int
    hosts_up : float
    results : list[HostResult]



@app.get("/")
def serve_frontend():
    return FileResponse("web/index.html")

@app.get("/ports")
def get_common_ports():
    """Return the list of common ports so the frontend can display them."""
    return {
        "ports": [
            {"port": port, "service": service}
            for port, service in COMMON_SERVICE_PORTS.items()
        ]
    }

@app.post("/scan")
def run_scan(request : ScanRequest):
    ports = parse_ports(request.ports)

    try:
        results = ful_scan(
            target_ip = request.target,
            ports = ports,
            port_workers=request.threads,
            ping_workers=request.ping_threads,
            timeout=request.timeout
        )
        return results
    except ValueError as e:
        return {"error" : str(e)}

    except Exception as e:
        return {"error" : f"Scan failed with error: {str(e)}"}


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Network Scanner API is running"}

def parse_ports(port_string: str) -> List[int]:
    if not port_string or port_string.lower() == "common":
        return list(COMMON_SERVICE_PORTS.keys())

    ports = set()

    for part in port_string.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                start, end = int(start.strip()), int(end.strip())
                if start > end or start < 1 or end > 65535:
                    raise ValueError
                ports.update(range(start, end + 1))
            except ValueError:
                pass  # skip invalid ranges silently in API mode
        else:
            try:
                port = int(part)
                if 1 <= port <= 65535:
                    ports.add(port)
            except ValueError:
                pass

    return sorted(ports) if ports else list(COMMON_SERVICE_PORTS.keys())
