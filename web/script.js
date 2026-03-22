const COMMON_PORTS = [
    { port: 21,   service: "FTP"       },
    { port: 22,   service: "SSH"       },
    { port: 23,   service: "Telnet"    },
    { port: 25,   service: "SMTP"      },
    { port: 53,   service: "DNS"       },
    { port: 80,   service: "HTTP"      },
    { port: 110,  service: "POP3"      },
    { port: 135,  service: "RPC"       },
    { port: 139,  service: "NetBIOS"   },
    { port: 143,  service: "IMAP"      },
    { port: 443,  service: "HTTPS"     },
    { port: 445,  service: "SMB"       },
    { port: 993,  service: "IMAPS"     },
    { port: 995,  service: "POP3S"     },
    { port: 1723, service: "PPTP"      },
    { port: 3306, service: "MySQL"     },
    { port: 3389, service: "RDP"       },
    { port: 5900, service: "VNC"       },
    { port: 8080, service: "HTTP-Alt"  },
    { port: 8443, service: "HTTPS-Alt" },
];

let isScanning    = false;
let selectedPorts = new Set();

const scanBtn          = document.getElementById("scan-btn");
const statusDot        = document.getElementById("status-dot");
const statusText       = document.getElementById("status-text");
const loadingPanel     = document.getElementById("loading-panel");
const loadingMsg       = document.getElementById("loading-message");
const resultsPanel     = document.getElementById("results-panel");
const resultsContainer = document.getElementById("results-container");
const errorPanel       = document.getElementById("error-panel");
const errorMessage     = document.getElementById("error-message");
const statsBar         = document.getElementById("stats-bar");
const portsCount       = document.getElementById("ports-count");
const portsPreview     = document.getElementById("ports-preview");
const portTogglesDiv   = document.getElementById("port-toggles");

function buildPortToggles() {
    COMMON_PORTS.forEach(function(item) {
        var btn = document.createElement("button");
        btn.className    = "port-toggle selected";
        btn.dataset.port = item.port;
        btn.type         = "button";
        btn.innerHTML    =
            '<span class="port-toggle-number">' + item.port + '</span>' +
            '<span class="port-toggle-service">' + item.service + '</span>';

        btn.addEventListener("click", function() {
            togglePort(item.port, btn);
        });

        portTogglesDiv.appendChild(btn);
        selectedPorts.add(item.port);
    });

    updatePortsSummary();
}

function togglePort(port, btn) {
    if (selectedPorts.has(port)) {
        selectedPorts.delete(port);
        btn.classList.remove("selected");
    } else {
        selectedPorts.add(port);
        btn.classList.add("selected");
    }
    updatePortsSummary();
}

function selectAllPorts() {
    document.querySelectorAll(".port-toggle").forEach(function(btn) {
        btn.classList.add("selected");
        selectedPorts.add(parseInt(btn.dataset.port));
    });
    updatePortsSummary();
}

function clearAllPorts() {
    document.querySelectorAll(".port-toggle").forEach(function(btn) {
        btn.classList.remove("selected");
    });
    selectedPorts.clear();
    updatePortsSummary();
}

function updatePortsSummary() {
    var count = selectedPorts.size;
    portsCount.textContent = count;

    if (count === 0) {
        portsPreview.textContent = "none selected";
        portsPreview.style.color = "var(--red)";
    } else if (count === COMMON_PORTS.length) {
        portsPreview.textContent = "all common ports";
        portsPreview.style.color = "var(--accent)";
    } else {
        var sorted  = Array.from(selectedPorts).sort(function(a, b) { return a - b; });
        var preview = sorted.slice(0, 5).join(", ");
        var suffix  = sorted.length > 5 ? " +" + (sorted.length - 5) + " more" : "";
        portsPreview.textContent = preview + suffix;
        portsPreview.style.color = "var(--accent)";
    }
}

async function startScan() {
    if (isScanning) return;

    var target  = document.getElementById("target").value.trim();
    var threads = parseInt(document.getElementById("threads").value);
    var timeout = parseFloat(document.getElementById("timeout").value);

    if (!target) {
        showError("Please enter a target IP or subnet.");
        return;
    }

    if (selectedPorts.size === 0) {
        showError("Please select at least one port.");
        return;
    }

    var ports = Array.from(selectedPorts)
        .sort(function(a, b) { return a - b; })
        .join(",");

    isScanning = true;
    setStatus("scanning");
    showLoading("SCANNING " + target.toUpperCase() + "...");
    hideResults();
    hideError();
    disableButton();

    try {
        var response = await fetch("/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                target:       target,
                ports:        ports,
                threads:      threads,
                ping_threads: 50,
                timeout:      timeout
            })
        });

        var data = await response.json();

        if (data.error) {
            showError(data.error);
            setStatus("error");
            return;
        }

        displayStats(data);
        displayResults(data);
        setStatus("ready");

    } catch (err) {
        showError("Could not connect to scanner API. Is the server running?");
        setStatus("error");
    } finally {
        isScanning = false;
        hideLoading();
        enableButton();
    }
}

function displayStats(data) {
    document.getElementById("stat-target").textContent  = data.target;
    document.getElementById("stat-scanned").textContent = data.hosts_scanned;
    document.getElementById("stat-up").textContent      = data.hosts_up;
    document.getElementById("stat-time").textContent    = data.scan_time + "s";
    statsBar.style.display = "grid";
}

function displayResults(data) {
    resultsContainer.innerHTML = "";

    if (!data.results || data.results.length === 0) {
        resultsContainer.innerHTML =
            '<div class="no-ports-msg">No live hosts found in the scanned range.</div>';
        resultsPanel.style.display = "block";
        return;
    }

    data.results.forEach(function(host) {
        resultsContainer.appendChild(buildHostCard(host));
    });

    resultsPanel.style.display = "block";
}

function buildHostCard(host) {
    var card      = document.createElement("div");
    card.className = "host-card";

    var hostname  = host.hostname
        ? '<span class="host-hostname">(' + host.hostname + ')</span>'
        : "";
    var badgeText = host.port_count > 0
        ? host.port_count + " PORT" + (host.port_count > 1 ? "S" : "") + " OPEN"
        : "NO OPEN PORTS";
    var badgeClass = host.port_count > 0 ? "up" : "no-ports";

    card.innerHTML =
        '<div class="host-header">' +
        '<div>' +
        '<span class="host-ip">' + host.ip + '</span>' +
        hostname +
        '</div>' +
        '<span class="host-badge ' + badgeClass + '">' + badgeText + '</span>' +
        '</div>';

    if (host.open_ports && host.open_ports.length > 0) {
        var table      = document.createElement("table");
        table.className = "ports-table";
        table.innerHTML =
            '<thead><tr>' +
            '<th>PORT</th><th>STATE</th><th>SERVICE</th><th>BANNER / VERSION</th>' +
            '</tr></thead>';

        var tbody = document.createElement("tbody");

        host.open_ports.forEach(function(p) {
            var banner = p.banner
                ? p.banner.split("\n")[0].substring(0, 60)
                : "";
            var row = document.createElement("tr");
            row.innerHTML =
                '<td><span class="port-number">'  + p.port    + '</span></td>' +
                '<td><span class="port-state">'   + p.state   + '</span></td>' +
                '<td><span class="port-service">' + p.service + '</span></td>' +
                '<td><span class="port-banner">'  + banner    + '</span></td>';
            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        card.appendChild(table);
    } else {
        card.innerHTML +=
            '<div class="no-ports-msg">No open ports detected in scanned range.</div>';
    }

    return card;
}

function setStatus(state) {
    statusDot.className = "status-dot";
    if (state === "scanning") {
        statusDot.classList.add("scanning");
        statusText.textContent = "SCANNING";
        statusText.style.color = "var(--yellow)";
    } else if (state === "error") {
        statusDot.classList.add("error");
        statusText.textContent = "ERROR";
        statusText.style.color = "var(--red)";
    } else {
        statusText.textContent = "READY";
        statusText.style.color = "var(--green)";
    }
}

function showLoading(msg) {
    loadingMsg.textContent    = msg;
    loadingPanel.style.display = "block";
}

function hideLoading()  { loadingPanel.style.display  = "none"; }
function hideError()    { errorPanel.style.display    = "none"; }
function hideResults()  {
    resultsPanel.style.display = "none";
    statsBar.style.display     = "none";
    resultsContainer.innerHTML = "";
}

function showError(msg) {
    errorMessage.textContent  = msg;
    errorPanel.style.display  = "flex";
}

function disableButton() {
    scanBtn.disabled = true;
    scanBtn.querySelector(".btn-text").textContent = "SCANNING...";
}

function enableButton() {
    scanBtn.disabled = false;
    scanBtn.querySelector(".btn-text").textContent = "INITIATE SCAN";
}

document.getElementById("target").addEventListener("keydown", function(e) {
    if (e.key === "Enter") startScan();
});

buildPortToggles();