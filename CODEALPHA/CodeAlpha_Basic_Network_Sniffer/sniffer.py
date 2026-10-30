

"""
Basic Network Sniffer - 
CodeAlpha Cybersecurity Internship

Features:
- Live packet capture
- IPv4 / IPv6 address extraction
- TCP / UDP / ICMP / ARP identification
- TCP flag inspection
- DNS query and response analysis
- PCAP export
- Optional limited hexadecimal payload preview
"""

from datetime import datetime
from pathlib import Path

from scapy.all import (
    sniff,
    conf,
    IP,
    IPv6,
    TCP,
    UDP,
    ICMP,
    ARP,
    DNS,
    DNSQR,
    Raw,
    wrpcap,
)


# ==================================================
# CONFIGURATION
# ==================================================

INTERFACE_INDEX = 3

PACKET_COUNT = 10
CAPTURE_TIMEOUT = 30

# None = capture all traffic.
# Examples: "tcp", "udp", "icmp", "port 53"
BPF_FILTER = "udp port 53"

SAVE_PCAP = True

# Payload previews can expose sensitive information.
# Keep disabled unless you have a specific reason.
SHOW_PAYLOAD_PREVIEW = False
MAX_PAYLOAD_BYTES = 32

CAPTURE_DIRECTORY = Path("captures")


# ==================================================
# PACKET ANALYSIS
# ==================================================

def get_addresses(packet):
    """Extract source and destination addresses."""

    if IP in packet:
        return packet[IP].src, packet[IP].dst

    if IPv6 in packet:
        return packet[IPv6].src, packet[IPv6].dst

    if ARP in packet:
        return packet[ARP].psrc, packet[ARP].pdst

    return "Unknown", "Unknown"


def analyze_dns(packet):
    """Extract DNS query and response information."""

    dns = packet[DNS]

    if dns.qr == 0:
        message_type = "DNS Query"
    else:
        message_type = "DNS Response"

    domain = "Unknown"

    if dns.qd is not None and DNSQR in dns:
        try:
            domain = dns.qd.qname.decode(
                "utf-8", errors="replace"
            ).rstrip(".")
        except (AttributeError, UnicodeError):
            domain = "Could not decode"

    details = [
        f"DNS Type: {message_type}",
        f"Domain: {domain}",
    ]

    if dns.qr == 1:
        details.append(f"Response Code: {dns.rcode}")
        details.append(f"Answer Count: {dns.ancount}")

    return details


def analyze_packet(packet):
    """Display useful information about a captured packet."""

    timestamp = datetime.fromtimestamp(
        float(packet.time)
    ).strftime("%Y-%m-%d %H:%M:%S")

    source, destination = get_addresses(packet)

    protocol = "Other"
    details = []

    # DNS is an application-layer protocol.
    # Check it before TCP and UDP classification.
    if DNS in packet:
        protocol = "DNS"
        details.extend(analyze_dns(packet))

    elif TCP in packet:
        protocol = "TCP"

        tcp = packet[TCP]

        details.append(
            f"Source Port: {tcp.sport}"
        )

        details.append(
            f"Destination Port: {tcp.dport}"
        )

        details.append(
            f"TCP Flags: {tcp.flags}"
        )

    elif UDP in packet:
        protocol = "UDP"

        udp = packet[UDP]

        details.append(
            f"Source Port: {udp.sport}"
        )

        details.append(
            f"Destination Port: {udp.dport}"
        )

    elif ICMP in packet:
        protocol = "ICMP"

        icmp = packet[ICMP]

        details.append(
            f"ICMP Type: {icmp.type}"
        )

        details.append(
            f"ICMP Code: {icmp.code}"
        )

    elif ARP in packet:
        protocol = "ARP"

        arp = packet[ARP]

        operation = {
            1: "Request",
            2: "Reply",
        }.get(arp.op, str(arp.op))

        details.append(
            f"ARP Operation: {operation}"
        )

    elif IPv6 in packet:
        protocol = "IPv6"

    elif IP in packet:
        protocol = "IP"

    # Display packet information.
    print("\n" + "=" * 55)
    print(f"Timestamp:   {timestamp}")
    print(f"Protocol:    {protocol}")
    print(f"Source:      {source}")
    print(f"Destination: {destination}")
    print(f"Packet Size: {len(packet)} bytes")

    for detail in details:
        print(detail)

    # Optional limited payload preview.
    if SHOW_PAYLOAD_PREVIEW and Raw in packet:
        payload = bytes(packet[Raw].load)
        preview = payload[:MAX_PAYLOAD_BYTES]

        print(
            "Payload (hex):",
            preview.hex(" ")
        )

        if len(payload) > MAX_PAYLOAD_BYTES:
            print("Payload preview truncated.")

    print("=" * 55)


# ==================================================
# MAIN CAPTURE FUNCTION
# ==================================================

def main():

    print("\n" + "=" * 55)
    print("             BASIC NETWORK SNIFFER")
    print("             CODEALPHA - VERSION 3")
    print("=" * 55)

    interface = conf.ifaces.dev_from_index(
        INTERFACE_INDEX
    )

    if interface is None:
        print("ERROR: Network interface not found.")
        return

    print(f"Interface: {interface.name}")
    print(f"Packet Limit: {PACKET_COUNT}")
    print(f"Timeout: {CAPTURE_TIMEOUT} seconds")
    print(f"BPF Filter: {BPF_FILTER or 'All traffic'}")

    print("\nStarting packet capture...")
    print("Generate network traffic to observe packets.")
    print("Press CTRL+C to stop.\n")

    try:

        packets = sniff(
            iface=interface,
            prn=analyze_packet,
            count=PACKET_COUNT,
            timeout=CAPTURE_TIMEOUT,
            filter=BPF_FILTER,
            store=True,
        )

        print("\nCapture completed.")

    except KeyboardInterrupt:

        print("\nCapture interrupted by user.")
        return

    except PermissionError:

        print("\nERROR: Administrator privileges required.")
        return

    except Exception as error:

        print(f"\nCapture error: {error}")
        return

    print(f"Total packets captured: {len(packets)}")

    # Save captured packets.
    if SAVE_PCAP and packets:

        try:

            CAPTURE_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = (
                "capture_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".pcap"
            )

            output_path = CAPTURE_DIRECTORY / filename

            wrpcap(str(output_path), packets)

            print(f"PCAP saved: {output_path}")

        except Exception as error:

            print(f"PCAP export error: {error}")

    elif SAVE_PCAP:

        print("No packets captured. PCAP not created.")

    print("\nSniffer stopped.")


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
