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