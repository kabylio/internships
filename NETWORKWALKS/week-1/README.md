# NetworkWalks Week 1 Cybersecurity Lab Setup

## Overview

This project documents the network baseline established for a Kali Linux virtual machine in a VMware Workstation environment. The goal of the lab was to confirm the guest had a valid network configuration, could reach the default gateway, and could establish outbound connectivity to external services over the VMware NAT network.

The environment used VMware NAT and a DHCP-assigned IPv4 address. This was a practical lab setup that enabled network validation without creating a second VM or additional host-side configuration.

## Lab objectives

The Week 1 lab focused on validating the following cybersecurity and networking fundamentals:

- Interface identification and status verification
- DHCP-based IP acquisition in a Linux guest
- Route and gateway verification
- Connectivity testing to local and external targets
- DNS resolution validation
- HTTPS request verification
- Evidence collection for technical documentation and portfolio submission

## Environment summary

| Item | Value |
| --- | --- |
| Platform | Virtualbox |
| Guest OS | Kali Linux |
| Interface | `eth0` |
| IP configuration | DHCP |
| IPv4 address | `192.168.154.132/24` |
| Gateway | `192.168.154.2` |
| Subnet | `192.168.154.0/24` |
| Network mode | NAT |
| Snapshot name | `Kali - NetworkWalks Baseline` |

## Network architecture

The Kali guest was connected to the  NAT network. The guest received an IP address from the VMware DHCP service and used the NAT gateway for outbound connectivity.

```mermaid
flowchart LR
    A[Internet / External Network] --> B[Gateway 192.168.154.2]
    B --> C[ NAT ]
    C --> D[Kali Linux eth0 192.168.154.132/24]
