# Basic Network Sniffer



**CodeAlpha Cybersecurity Internship - Project 1**



A Python-based network sniffer built with Scapy to capture, inspect, and export network packets for basic network traffic analysis.



## Features



- Live packet capture using Scapy.

- IPv4, IPv6, and ARP address extraction.

- TCP, UDP, ICMP, and ARP protocol identification.

- TCP port and flag inspection.

- DNS query and response parsing.

- Configurable network interface, packet limit, timeout, and BPF filter.

- Optional hexadecimal payload preview.

- PCAP export for further analysis using Wireshark.



## Technology Stack



- Python 3.13.5

- Scapy 2.8.0

- Npcap



## Project Structure



```text

Basic-Network-Sniffer/

├──  .gitignore
│
├──  requirements.txt
│
├──  sniffer.py
│
└── README.md

```



## Requirements



- Python 3.10 or later.

- Npcap installed on Windows.

- Administrator privileges may be required for packet capture.



## Installation



Create a virtual environment:



```powershell

python -m venv .venv

..venvScriptsActivate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



## Configuration



Review these settings in `sniffer.py`:



- `INTERFACE_INDEX`: network interface to monitor.

- `PACKET_COUNT`: maximum number of packets.

- `CAPTURE_TIMEOUT`: capture duration in seconds.

- `BPF_FILTER`: Berkeley Packet Filter expression.

- `SAVE_PCAP`: enables or disables PCAP export.



**Important:** Network interface indexes are machine-specific. Check and adjust the configured index for your computer.



The current configuration uses:



```python

BPF_FILTER = "udp port 53"

```



Other examples:



```python

BPF_FILTER = "tcp"

BPF_FILTER = "icmp"

BPF_FILTER = "port 443"

BPF_FILTER = None

```



## Usage



Open PowerShell as Administrator, activate the virtual environment, and execute:



```powershell

python .sniffer.py

```



The application displays packet information in the terminal and exports captured packets to the `captures/` directory when PCAP saving is enabled.



## Testing and Validation



Version 3 was tested on Windows.



Observed tests included:



- TCP, UDP, and ICMP packet capture.

- DNS query and response parsing.

- Configurable packet capture and filtering.

- PCAP file export.

- Separate Windows PowerShell investigation of a TCP connection's owning process.



These tests demonstrate selected functionality, not exhaustive protocol coverage or a formal security audit.



## Limitations



- Basic packet inspection rather than full protocol dissection.

- No TLS or encrypted application payload decryption.

- No automated process attribution.

- Packet visibility depends on the selected interface, permissions, network configuration, and capture filter.



## Security and Ethical Use



Use this tool only on networks and systems you own or have explicit authorization to monitor.



Packet captures can contain sensitive information. PCAP files are excluded from Git and should be stored securely.



## Project Status



**Version 3 - Tested baseline**



Future development may introduce improved architecture, packet statistics, structured logging, and additional analysis capabilities.



## Author



**Mohamed Farid Menasria**



GitHub: [@kabylio](https://github.com/kabylio)



Developed as part of the CodeAlpha Cybersecurity Internship.
