# Port Scanner - Project Plan

## What is this project?

A beginner-friendly port scanner built in Python. It checks which network "doors" (ports) are open on a computer. Great for learning how networks really work.

## What problem does it solve?

You want to understand:
- How computers connect to each other
- What ports are and why they matter
- How TCP actually works at the socket level

Instead of reading about it, you can see it in action.

## What the tool should do

### Core features

1. **Scan a target** - Take an IP address or website name
2. **Check ports** - Look for open ports on that target
3. **Show results** - Display what it found in a clean way
4. **Be fast** - Use threading to scan multiple ports at once

### Ways to use it

| Command | What it does |
|---------|--------------|
| `--quick` | Scan only the top 20 most common ports |
| `-p 1-100` | Scan a specific range |
| `-p all` | Scan all 65,535 ports (takes a long time!) |
| `-t 50` | Use 50 threads instead of 10 for speed |

## How it works (technical)

- Uses Python's built-in `socket` library (no extra downloads)
- TCP Connect Scan: Actually tries to connect, more reliable than just sending a packet
- Threading: Check multiple ports simultaneously instead of one-by-one
- Timeout handling: Don't wait forever on ports that don't respond

## What gets scanned

**Default (common ports):**
21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 8080, 8443

**Quick preset (top 20):** First 20 common ports

**All ports:** 1 through 65535

## What the output looks like

```
============================================================
Port Scanner - Scan Report
============================================================
Target:      localhost (127.0.0.1)
Ports:       18
Scan Type:   Common Ports
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

## Project structure

```
port_scanner/
├── port_scanner.py   # Main code
├── SPEC.md          # This file
└── README.md        # User-facing documentation
```

## Key functions

| Function | Purpose |
|----------|---------|
| `scan_port()` | Try to connect to one port |
| `resolve_target()` | Convert website name to IP |
| `threaded_scan()` | Scan multiple ports at once |
| `parse_port_range()` | Understand user input like "1-100" |

## Things to keep in mind

- **Educational only** - Never scan without permission
- **Timeouts matter** - Too short misses slow ports, too long is slow
- **Threads have limits** - Too many threads can cause errors
- **Firewall can fool you** - Some firewalls don't respond at all

## Future ideas (not implemented yet)

- UDP scanning (different protocol, more complex)
- OS fingerprinting (guess what operating system)
- Service version detection (not just "HTTP" but "Apache 2.4")
- Save results to file
- GUI interface

## Security note

This is a LEARNING tool. The code is intentionally simple and well-commented. Real port scanners used by professionals have many more features, but this is meant to show the fundamentals.
