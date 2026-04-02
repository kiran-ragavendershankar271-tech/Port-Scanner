# TCP Port Scanner

A simple tool that helps you understand how computers communicate over networks. Perfect for beginners learning cybersecurity!

> **Think of it like this:** A port scanner is like knocking on doors in an apartment building to see who's home. Each door is a "port" and the person who answers tells you something useful.

## What does this actually do?

When you visit a website, your computer connects to their server through specific "doors" (ports). This tool lets you check which doors are open on any computer - kind of like walking around a building and checking which apartment lights are on.

## What you'll learn building this

- How TCP connections actually work (the famous "3-way handshake")
- What sockets are and how programs talk over networks
- How ports work (port 80 for websites, port 22 for SSH, etc.)
- Why threading makes scanning faster

## How to use it

```bash
# Scan your own computer (try this first!)
python port_scanner.py localhost --quick

# Check a website
python port_scanner.py google.com -p 80,443

# Scan a range of ports
python port_scanner.py localhost -p 1-100

# Scan with more speed (more threads)
python port_scanner.py localhost -p 1-1000 -t 50
```

## What the results mean

When you run a scan, you'll see something like:

```
PORT      STATUS    SERVICE
-----------------------------------
80        open      HTTP
443       open      HTTPS
22        closed    SSH
```

- **Open** = Something is listening on that port and willing to talk
- **Closed** = Nothing is listening, but the computer acknowledges the request
- **Filtered** = A firewall is blocking the request (no response at all)

## Common ports you might see

| Port | Service | Real-world example |
|------|---------|---------------------|
| 80 | HTTP | Regular websites |
| 443 | HTTPS | Secure websites (banking, login) |
| 22 | SSH | Remote command-line access |
| 21 | FTP | Old-school file transfers |
| 3389 | RDP | Windows remote desktop |

## What the scan actually shows

```
============================================================
Port Scanner - Scan Report
============================================================
Target:      localhost (127.0.0.1)
Ports:       18
Scan Type:   Quick (Top 20)
Start Time:  2026-04-02 14:23:00
------------------------------------------------------------

Scanning...
Scanning... 100.0% (18/18)

============================================================
Scan Complete - Found 3 open port(s)
Duration: 2.04 seconds
============================================================

PORT      STATUS    SERVICE
-----------------------------------
445       open      SMB
3389      open      RDP
3306      open      MySQL
```

## The 3-way handshake (simplified)

When you scan a port, here's what happens:

1. **Your computer**: "Hey, is anyone there?" (SYN)
2. **Target computer**: "Yes, I'm here!" (SYN-ACK)
3. **Your computer**: "Great, let's talk!" (ACK)

If the port is closed, you get a "No thanks" instead (RST).

## Important safety note

**Only scan computers you own or have permission to test.**

Scanning random websites or computers without permission is:
- Illegal in many places
- Considered an attack by security systems
- A quick way to get your IP banned

Think of it like this: It's fine to knock on your own door to see if anyone's home, but going around the neighborhood knocking on everyone's doors is creepy.

## Requirements

- Python 3.7 or higher
- That's it! No extra packages needed.

## What's in this project?

| File | What it is |
|------|------------|
| `port_scanner.py` | The main program - run this |
| `SPEC.md` | The design document (for developers) |
| `README.md` | This file - you're reading it! |

---

*Built to learn. Have fun experimenting!*
