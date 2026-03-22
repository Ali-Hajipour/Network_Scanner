# 🔍 Network Scanner — CLI & Web Application

> A professional-grade, multi-threaded TCP network scanner built entirely from scratch in Python — featuring both a powerful command line interface and a real-time web dashboard powered by FastAPI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-Educational-orange?style=flat-square)](LICENSE)

> ⚠️ **Legal notice:** Only scan networks you own or have explicit written permission to scan. Unauthorized scanning is illegal.

---

## 📸 Preview
General UI of the Netscan :
<img width="1918" height="956" alt="Screenshot 2026-03-22 at 18 28 45" src="https://github.com/user-attachments/assets/515ae777-7163-4577-8758-99091b8a00c2" />

<img width="1914" height="960" alt="Screenshot 2026-03-22 at 18 30 52" src="https://github.com/user-attachments/assets/c473eeab-f9fd-4c2d-8c16-420caae41cbf" />
<img width="1919" height="957" alt="Screenshot 2026-03-22 at 18 31 48" src="https://github.com/user-attachments/assets/7dabb5af-0903-4112-9dfb-4e3fc7fa112a" />

Tried for cispa.de : 
<img width="1886" height="940" alt="Screenshot 2026-03-22 at 18 32 31" src="https://github.com/user-attachments/assets/7dfe0690-935f-4cc9-9cf9-58cdc52608d9" />
<img width="1907" height="945" alt="Screenshot 2026-03-22 at 18 32 50" src="https://github.com/user-attachments/assets/fe6f2153-7891-414b-b5ae-5d75dfdb58db" />






---

## 🌟 What is this?

This project is a fully functional network scanner — similar to Nmap — built entirely from scratch without using any existing scanning libraries. It demonstrates deep understanding of:

- How TCP/IP connections work at the socket level
- How to discover live hosts on a network
- How to identify running services by their banners
- How to build a REST API that connects a Python backend to a web frontend
- How to use threading to scan hundreds of ports simultaneously

The project has **two interfaces** — a command line tool for quick terminal use, and a full web application with a dark-themed dashboard that displays scan results in real time.

---

## ✨ Features

### 🔎 Scanning Engine
- **Host discovery** — ICMP ping sweep discovers all live hosts across entire subnets (e.g. `192.168.1.0/24`) simultaneously
- **TCP port scanning** — full 3-way handshake connect scan across configurable port selections
- **Banner grabbing** — passive read for services that announce themselves (SSH, FTP, SMTP), active HTTP probe for web servers
- **Service identification** — maps 20 common ports to their service names (FTP, SSH, HTTP, HTTPS, MySQL, RDP etc.)
- **Reverse DNS lookup** — resolves IP addresses to hostnames (e.g. `192.168.1.1` → `router.local`)

### ⚡ Performance
- **Multi-threaded** — concurrent scanning with `ThreadPoolExecutor` (100+ threads by default)
- **Configurable threads** — tune thread count from 1 to 500 depending on network conditions
- **Configurable timeout** — adjust per-port timeout from 0.1s to 10s
- **Parallel host discovery** — pings entire subnet simultaneously instead of sequentially

### 🌐 Web Application
- **Real-time dashboard** — results appear as scan completes
- **Port toggle selector** — click individual ports to include/exclude from scan
- **Select All / Clear** — quickly configure all ports with one click
- **Live status indicator** — animated status dot shows Ready / Scanning / Error states
- **Scan summary stats** — shows target, hosts scanned, hosts up, and elapsed time
- **Results table** — clean table per host showing port, state, service, and banner
- **Error handling** — friendly error messages for invalid targets or connection failures

### 💾 Output
- **JSON export** — structured scan report with metadata saved to disk
- **CLI table output** — formatted terminal output with aligned columns
- **REST API** — programmatic access to all scanner features via HTTP

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Scanner engine | Python 3, `socket` | Raw TCP connections and port scanning |
| Host discovery | `subprocess`, `platform` | Cross-platform ICMP ping sweep |
| Concurrency | `concurrent.futures` | Parallel scanning with thread pools |
| Networking | `ipaddress` | Subnet parsing and IP math |
| Web backend | FastAPI, Uvicorn | REST API serving scan results |
| Data validation | Pydantic | Request/response models |
| Web frontend | HTML5, CSS3 | Dashboard structure and styling |
| Frontend logic | Vanilla JavaScript | Fetch API, DOM manipulation, state management |
| CLI | `argparse` | Command line interface |
| Data export | `json`, `datetime` | Structured JSON report generation |

---

## 📁 Project Structure

```
network-scanner/
│
├── scanner.py          # Core scanning engine
│   ├── ping_host()         → ICMP ping single host
│   ├── discover_hosts()    → sweep entire subnet
│   ├── scan_port()         → TCP connect to single port
│   ├── grab_banner()       → read service banner
│   ├── scan_host_ports()   → scan all ports on one host
│   └── ful_scan()          → orchestrate full scan
│
├── reporter.py         # Output and export
│   ├── print_summary()     → formatted terminal output
│   ├── save_report()       → JSON file export
│   └── load_report()       → load saved JSON report
│
├── main.py             # CLI entry point
│   ├── parse_ports()       → convert port string to list
│   └── main()              → argparse CLI interface
│
├── api.py              # FastAPI web backend
│   ├── GET  /              → serve web dashboard
│   ├── POST /scan          → run scan, return JSON
│   ├── GET  /ports         → list common ports
│   └── GET  /health        → health check
│
└── web/                # Frontend web application
    ├── index.html          → dashboard structure
    ├── style.css           → dark terminal aesthetic styling
    └── script.js           → port toggles, fetch API, results rendering
```

---

## 🚀 Installation

**Requirements:** Python 3.8+, pip

```bash
# 1. Clone the repository
git clone https://github.com/Ali-Hajipour/Network_Scanner.git
cd Network_Scanner

# 2. Install dependencies
pip install fastapi uvicorn

# 3. You're ready to go
```

---

## 💻 Usage

### 🌐 Option 1 — Web Application

```bash
uvicorn api:app --reload
```

Open your browser at: **http://localhost:8000**

**Steps:**
1. Enter a target IP (`192.168.1.1`) or subnet (`192.168.1.0/24`)
2. Select which ports to scan using the toggle buttons
3. Adjust threads and timeout if needed
4. Click **INITIATE SCAN**
5. Watch results appear in real time

You can also explore the **auto-generated API documentation** at:
```
http://localhost:8000/docs
```

---

### ⌨️ Option 2 — Command Line Interface

```bash
# Scan common ports on a single host
python main.py 192.168.1.1

# Scan an entire /24 subnet
python main.py 192.168.1.0/24

# Scan specific ports only
python main.py 192.168.1.1 -p 22,80,443

# Scan a full port range
python main.py 192.168.1.0/24 -p 1-1024

# Save results as JSON
python main.py 192.168.1.0/24 -o results.json

# Fast scan with more threads and lower timeout
python main.py 192.168.1.0/24 --threads 200 --timeout 0.5

# Show all options
python main.py --help
```

**Example terminal output:**
```
============================================================
  Network Scanner v1.0  —  Phase 1 (Core)
============================================================
  Target  : 192.168.1.0/24
  Ports   : 20 port(s) selected
  Threads : 100 (port) / 50 (ping)
  Timeout : 1.0s per port
============================================================

[*] Scanning 254 hosts in 192.168.1.0/24...
  [+] Host up: 192.168.1.1
  [+] Host up: 192.168.1.5

[*] Port scanning 192.168.1.1...
  PORT     STATE    SERVICE      BANNER
  ────────────────────────────────────────────────────
  22       open     SSH          SSH-2.0-OpenSSH_8.9
  80       open     HTTP         HTTP/1.1 200 OK

============================================================
  SCAN COMPLETE
============================================================
  Target        : 192.168.1.0/24
  Hosts scanned : 254
  Hosts up      : 2
  Scan time     : 14.35s
============================================================
```

---

## 🔌 REST API Reference

### POST `/scan`

Run a network scan and receive structured JSON results.

**Request body:**
```json
{
    "target": "192.168.1.1",
    "ports": "22,80,443",
    "threads": 100,
    "ping_threads": 50,
    "timeout": 1.0
}
```

**Response:**
```json
{
    "target": "192.168.1.1",
    "scan_time": 2.34,
    "hosts_scanned": 1,
    "hosts_up": 1,
    "results": [
        {
            "ip": "192.168.1.1",
            "hostname": "router.local",
            "status": "up",
            "port_count": 2,
            "open_ports": [
                {
                    "port": 22,
                    "state": "open",
                    "service": "SSH",
                    "banner": "SSH-2.0-OpenSSH_8.9"
                },
                {
                    "port": 80,
                    "state": "open",
                    "service": "HTTP",
                    "banner": "HTTP/1.1 200 OK"
                }
            ]
        }
    ]
}
```

### All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`       | Serves the web dashboard HTML |
| `POST` | `/scan`   | Runs a scan, returns JSON results |
| `GET`  | `/ports`  | Returns list of all common ports |
| `GET`  | `/health` | Server health check |

---

## 🧠 How It Works

### Host Discovery
```
Your machine ──── ICMP ping ────→ 192.168.1.1
             ←─── reply ────────               alive ✅

Your machine ──── ICMP ping ────→ 192.168.1.2
             [silence]                          dead ❌
```
254 pings run simultaneously using threads — entire subnet discovered in ~2 seconds.

### Port Scanning (TCP Connect Scan)
```
Your machine ──── SYN ─────────→ target:80
             ←─── SYN-ACK ──────             port OPEN ✅

Your machine ──── SYN ─────────→ target:9999
             ←─── RST ───────────             port CLOSED ❌

Your machine ──── SYN ─────────→ target:443
             [silence / timeout]               port FILTERED 🔥
```

### Banner Grabbing
```
Connect to port 22 → server sends "SSH-2.0-OpenSSH_8.9"  → passive read
Connect to port 80 → silence → send HTTP request → read response headers
```

---

## 🗺️ Roadmap

- [x] **Phase 1** — Core scanner (ping sweep, TCP scan, banner grab, web UI, REST API)
- [ ] **Phase 2** — OS fingerprinting (TTL analysis, TCP window size detection)
- [ ] **Phase 3** — CVE lookup (NVD API integration, vulnerability reporting)
- [ ] **Phase 4** — Docker support, GitHub Actions CI/CD pipeline

---

## ⚙️ CLI Options Reference

| Flag | Default | Description |
|------|---------|-------------|
| `target` | required | IP address or subnet in CIDR notation |
| `-p, --port` | `common` | Ports: `common`, `80`, `22,80,443`, `1-1024` |
| `--threads` | `100` | Concurrent threads for port scanning |
| `--ping-threads` | `50` | Concurrent threads for ping sweep |
| `--timeout` | `1.0` | TCP connection timeout per port (seconds) |
| `-o, --output` | None | Save results as JSON to this file |

---

## 🔒 Legal & Ethical Use

This tool is built for:
- Learning network programming and security concepts
- Scanning your own home or lab network
- Authorized penetration testing with written permission

**Never use this tool on networks you do not own or have explicit permission to scan.**
Unauthorized port scanning is illegal in most countries.

---

## 👤 Author

**Ali Hajipour**
- 🐙 GitHub: [@Ali-Hajipour](https://github.com/Ali-Hajipour)
- 💼 LinkedIn: [*(alihajipour-it)*](https://www.linkedin.com/in/alihajipour-it/)

---

## 📄 License

This project is for educational purposes only.
Only scan networks you own or have explicit written permission to scan.
