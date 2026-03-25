# 🔍 Netzwerk-Scanner — CLI & Web-Anwendung

> Ein professioneller, multi-threaded TCP-Netzwerk-Scanner, komplett von Grund auf in Python entwickelt — mit leistungsstarker Kommandozeile und einem Echtzeit-Web-Dashboard auf Basis von FastAPI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-Educational-orange?style=flat-square)](LICENSE)

> ⚠️ **Rechtlicher Hinweis:** Scannen Sie nur Netzwerke, die Ihnen gehören oder für die Sie eine ausdrückliche schriftliche Erlaubnis haben. Unerlaubtes Scannen ist illegal.

---

## 📸 Vorschau

Allgemeine Benutzeroberfläche des Netscanners:

![Dashboard Übersicht](https://github.com/user-attachments/assets/515ae777-7163-4577-8758-99091b8a00c2)
![Scan-Ergebnisse](https://github.com/user-attachments/assets/c473eeab-f9fd-4c2d-8c16-420caae41cbf)
![Port-Ansicht](https://github.com/user-attachments/assets/7dabb5af-0903-4112-9dfb-4e3fc7fa112a)

Getestet auf cispa.de:

![cispa.de Test 1](https://github.com/user-attachments/assets/7dfe0690-935f-4cc9-9cf9-58cdc52608d9)
![cispa.de Test 2](https://github.com/user-attachments/assets/fe6f2153-7891-414b-b5ae-5d75dfdb58db)

---

## 🌟 Was ist das?

Dieses Projekt ist ein voll funktionsfähiger Netzwerk-Scanner — vergleichbar mit Nmap —, der komplett von Grund auf ohne Verwendung bestehender Scanning-Bibliotheken entwickelt wurde. Es demonstriert ein tiefes Verständnis von:

- TCP/IP-Verbindungen auf Socket-Ebene
- Erkennung aktiver Hosts in einem Netzwerk
- Identifikation laufender Dienste durch Banner-Grabbing
- Erstellung einer REST-API, die Backend und Web-Frontend verbindet
- Threading für gleichzeitiges Scannen von Hunderten Ports

Das Projekt bietet **zwei Oberflächen**: ein Kommandozeilen-Tool für schnelle Terminal-Nutzung und eine vollwertige Web-Anwendung mit einem dunklen Dashboard, das Ergebnisse in Echtzeit anzeigt.

---

## ✨ Funktionen

### 🔎 Scanning-Engine

- **Host Discovery** — ICMP-Ping-Sweep entdeckt alle aktiven Hosts in ganzen Subnetzen (z. B. `192.168.1.0/24`) gleichzeitig
- **TCP-Port-Scanning** — vollständiger 3-Way-Handshake-Connect-Scan mit konfigurierbaren Port-Auswahlen
- **Banner Grabbing** — passives Auslesen von Diensten (SSH, FTP, SMTP) und aktive HTTP-Probe für Webserver
- **Service-Erkennung** — Zuordnung von 20 gängigen Ports zu Dienstnamen (FTP, SSH, HTTP, HTTPS, MySQL, RDP etc.)
- **Reverse DNS Lookup** — Auflösung von IP-Adressen zu Hostnamen

### ⚡ Performance

- **Multi-Threaded** — paralleles Scannen mit `ThreadPoolExecutor` (standardmäßig 100+ Threads)
- **Konfigurierbare Threads** — von 1 bis 500 Threads je nach Netzwerkbedingungen
- **Konfigurierbares Timeout** — pro Port von 0,1 s bis 10 s
- **Parallele Host Discovery** — gesamtes Subnetz wird gleichzeitig gepingt

### 🌐 Web-Anwendung

- **Echtzeit-Dashboard** — Ergebnisse erscheinen während des Scans
- **Port-Toggle-Auswahl** — einzelne Ports per Klick ein-/ausschalten
- **Select All / Clear** — schnelle Konfiguration aller Ports
- **Live-Status-Indikator** — animierter Punkt zeigt Ready / Scanning / Error
- **Scan-Zusammenfassung** — Ziel, gescannte Hosts, erreichte Hosts und Dauer
- **Ergebnistabelle** — übersichtliche Tabelle pro Host (Port, Status, Dienst, Banner)
- **Fehlerbehandlung** — benutzerfreundliche Meldungen

### 💾 Ausgabe

- **JSON-Export** — strukturierter Scan-Report mit Metadaten
- **CLI-Tabellenausgabe** — formatierte Terminal-Ausgabe
- **REST-API** — programmatischer Zugriff auf alle Funktionen

---

## 🛠️ Technologie-Stack

| Schicht          | Technologie                  | Zweck                               |
|------------------|------------------------------|-------------------------------------|
| Scanner-Engine   | Python 3, `socket`           | Raw TCP-Verbindungen & Port-Scan    |
| Host Discovery   | `subprocess`, `platform`     | Plattformübergreifender ICMP-Ping   |
| Concurrency      | `concurrent.futures`         | Paralleles Scannen mit Thread-Pools |
| Networking       | `ipaddress`                  | Subnetz-Parsing & IP-Berechnungen   |
| Web-Backend      | FastAPI, Uvicorn             | REST-API & Dashboard                |
| Datenvalidierung | Pydantic                     | Request/Response-Modelle            |
| Web-Frontend     | HTML5, CSS3                  | Dashboard-Struktur & Design         |
| Frontend-Logik   | Vanilla JavaScript           | Fetch API, DOM & State-Management   |
| CLI              | `argparse`                   | Kommandozeilen-Schnittstelle        |
| Datenausgabe     | `json`, `datetime`           | Strukturierte JSON-Reports          |

---

## 📁 Projektstruktur

```
network-scanner/
│
├── scanner.py          # Kern-Scanning-Engine
├── reporter.py         # Ausgabe & Export
├── main.py             # CLI-Einstiegspunkt
├── api.py              # FastAPI Web-Backend
└── web/                # Frontend
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 🚀 Installation

**Voraussetzungen:** Python 3.8+, pip

```bash
git clone https://github.com/Ali-Hajipour/Network_Scanner.git
cd Network_Scanner
pip install fastapi uvicorn
```

---

## 💻 Nutzung

### 🌐 Option 1 — Web-Anwendung

```bash
uvicorn api:app --reload
```

Öffnen Sie im Browser: `http://localhost:8000`

### ⌨️ Option 2 — Kommandozeile

```bash
python main.py 192.168.1.1
python main.py 192.168.1.0/24 -p 22,80,443 --threads 200
python main.py --help
```

---

## 🔌 REST-API-Referenz

### `POST /scan`

Führt einen Netzwerk-Scan aus und gibt strukturierte JSON-Ergebnisse zurück.

**Request-Body:**

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

### Alle Endpunkte

| Methode | Endpunkt  | Beschreibung                          |
|---------|-----------|---------------------------------------|
| GET     | `/`       | Liefert das Web-Dashboard (HTML)      |
| POST    | `/scan`   | Führt Scan aus und gibt JSON zurück   |
| GET     | `/ports`  | Liste aller gängigen Ports            |
| GET     | `/health` | Server-Status-Check                   |

---

## 🧠 Funktionsweise

### Host Discovery

254 Pings laufen gleichzeitig mit Threads — gesamtes Subnetz wird in ~2 Sekunden entdeckt.

### Port Scanning (TCP Connect Scan)

Vollständiger 3-Way-Handshake: `SYN → SYN-ACK` (open) / `RST` (closed) / Timeout (filtered).

### Banner Grabbing

Passive Verbindung zu offenen Ports und Auslesen der Service-Banner (SSH, HTTP etc.).

---

## ⚙️ CLI-Optionen

| Flag              | Standard      | Beschreibung                                   |
|-------------------|---------------|------------------------------------------------|
| `target`          | erforderlich  | IP oder Subnetz (CIDR)                         |
| `-p`, `--port`    | `common`      | Ports: `common`, `80`, `22,80,443`, `1-1024`   |
| `--threads`       | `100`         | Threads für Port-Scan                          |
| `--ping-threads`  | `50`          | Threads für Ping-Sweep                         |
| `--timeout`       | `1.0`         | Timeout pro Port (Sekunden)                    |
| `-o`, `--output`  | `None`        | JSON-Datei speichern                           |

---

## 🗺️ Roadmap

- [x] Phase 1 — Kern-Scanner (Ping, TCP-Scan, Banner, Web-UI, REST-API)
- [ ] Phase 2 — OS-Fingerprinting (TTL-Analyse, TCP Window Size)
- [ ] Phase 3 — CVE-Lookup (NVD-API-Integration)
- [ ] Phase 4 — Docker & GitHub Actions CI/CD

---

## 🔒 Rechtliche & Ethische Nutzung

Dieses Tool dient ausschließlich:

- Lernzwecken im Bereich Netzwerkprogrammierung und IT-Security
- Scannen des eigenen Heim- oder Labornetzwerks
- Autorisierten Penetrationstests mit schriftlicher Erlaubnis

> ❌ Niemals auf fremden Netzwerken ohne ausdrückliche Genehmigung einsetzen.

---

## 👤 Autor

**Ali Hajipour**

- 🐙 GitHub: [@Ali-Hajipour](https://github.com/Ali-Hajipour)
- 💼 LinkedIn: [alihajipour-it](https://linkedin.com/in/alihajipour-it)

---

## 📄 Lizenz

Dieses Projekt dient ausschließlich Bildungszwecken. Scannen Sie nur Netzwerke, die Ihnen gehören oder für die Sie eine ausdrückliche schriftliche Erlaubnis haben.
