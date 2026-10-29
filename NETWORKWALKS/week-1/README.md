# Networkwalks Cybersecurity Internship — Week 1

## Project
Cybersecurity & Pentesting Lab Setup with VirtualBox and Kali Linux.

## Objective
Build a secure and functional cybersecurity lab environment using Kali Linux in VirtualBox, with a NAT network configured for controlled outbound access, a static Kali IP address, shared folders, clipboard support, drag-and-drop functionality, and a clean snapshot for recovery.

The lab was designed to provide a practical starting point for offensive security, networking, and system troubleshooting exercises while keeping the environment isolated enough for safe experimentation.

## Lab Environment

- Host platform: VirtualBox
- Guest OS: Kali Linux
- Network mode: NAT Network
- NAT subnet: `10.0.0.0/24`
- Kali static IP: `10.0.0.2/24`
- Shared folder: Windows Downloads mapped into Kali
- Shared clipboard: Enabled
- Drag-and-drop: Enabled

## Step-by-Step Setup

### 1. VirtualBox and Kali Installation
The pre-built Kali Linux VirtualBox image was imported and started successfully.

![VM running in VirtualBox](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20154412.png)

### 2. NAT Network Configuration
A NAT Network named `NatNetwork` was created using the IPv4 prefix `10.0.0.0/24`.

![NAT network settings](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20162643.png)

### 3. Kali VM Network Settings
The Kali VM was attached to `NatNetwork` and Promiscuous Mode was set to `Allow All` to ensure the guest could interact with the network as needed for the lab.

![Kali network adapter settings](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20162752.png)

### 4. Clipboard and Drag-and-Drop
Bidirectional shared clipboard and drag-and-drop were enabled to improve usability between the host and Kali guest.

![Clipboard and drag-and-drop settings](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20162940.png)

### 5. Shared Folders
A shared folder from the Windows host was mapped into the Kali VM and made available on the desktop for file transfer and lab workflow support.

![Shared folder configuration](screenshots/Copy%20of%20Capture%20d%27%C3%A9cran%202026-10-29%20163026.png)
![Shared folder on the desktop](screenshots/screenshot.jpg)

### 6. Static IP Configuration
A static IP address of `10.0.0.2/24` was configured in Kali using `nmcli`. This allowed the VM to have a consistent address within the lab network and ensured stable communication during testing and troubleshooting.

![Static IP and internet connectivity](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20163026.png)

### 7. Snapshot
A clean snapshot of the final working configuration was taken to create a reliable recovery point before further lab changes or troubleshooting.

![Snapshot of the completed lab](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20163026.png)

## Network Verification

The lab required the Kali VM to maintain connectivity to both the internal lab network and external internet resources. After the static IP configuration, the environment was validated and tested for reachability.

### Verified commands

```bash
ip addr
ip route
nmcli connection show
ping -c 3 10.0.0.1
ping -c 3 8.8.8.8
curl -I https://www.google.com
```

These checks confirmed that:
- the interface was active and assigned the correct IP
- the default route was present
- the network profile was valid
- the gateway was reachable
- external connectivity was working
- HTTPS services were reachable

## Troubleshooting

### Issue
After configuring the static IP address in Kali, the VM reported no internet access.

### Root cause
The issue was caused by a VirtualBox / Kali networking behavior related to DAD timeout handling after the static configuration was applied.

### Fix
The DAD timeout was disabled and the network interface was restarted to restore connectivity.

```bash
sudo nmcli connection modify "Wired connection 1" ipv4.dad-timeout 0
sudo nmcli connection down "Wired connection 1"
sudo nmcli connection up "Wired connection 1"
```

This reset the connection and restored the network path, allowing internet access to return.

## Snapshot and Recovery

The completed lab configuration was preserved with a VirtualBox snapshot named:

- `Kali - NetworkWalks Baseline`

This snapshot allows for quick rollback if future networking changes cause service interruption or misconfiguration.

## Skills Demonstrated

This project helped develop practical skills in:

- VirtualBox environment setup and VM configuration
- Kali Linux network configuration
- DHCP and static IP assignment
- NAT networking and route verification
- Shared folder and host-to-guest integration
- Troubleshooting connectivity issues in Linux
- Creating reusable lab snapshots for safe experimentation
- Technical documentation of a cybersecurity lab setup

## Notes

This lab served as a foundational step for later cybersecurity and pentesting work. It established a working, repeatable environment for learning network analysis, Linux troubleshooting, and security tooling in a controlled lab setup.
