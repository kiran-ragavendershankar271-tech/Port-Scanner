#!/usr/bin/env python3
"""
TCP Port Scanner - Beginner Cybersecurity Project

This tool demonstrates how TCP port scanning works at the socket level.
It attempts a full TCP connection (3-way handshake) to determine if a port is open.

EDUCATIONAL USE ONLY - Only scan hosts you own or have permission to test.
"""

import socket
import argparse
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Common port services for display purposes
PORT_SERVICES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
}

# Well-known ports for quick scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
                3306, 3389, 5432, 5900, 8080, 8443]


def scan_port(target: str, port: int, timeout: float = 1.0) -> dict:
    """
    Attempt TCP connection to a single port.

    This demonstrates the TCP 3-way handshake:
    1. Client sends SYN
    2. Server responds with SYN-ACK (if port is open)
    3. Client sends ACK to complete connection

    Args:
        target: IP address or hostname to scan
        port: Port number to check
        timeout: Seconds to wait for response

    Returns:
        Dictionary with port status and service name
    """
    result = {
        "port": port,
        "status": "closed",
        "service": PORT_SERVICES.get(port, "unknown")
    }

    try:
        # Create TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # attempt connection - this triggers TCP 3-way handshake
        connection_result = sock.connect_ex((target, port))

        # connect_ex returns 0 if successful (port is open)
        if connection_result == 0:
            result["status"] = "open"

        sock.close()

    except socket.timeout:
        result["status"] = "filtered"  # No response received
    except socket.error:
        pass  # Connection failed - port is closed
    except Exception:
        pass

    return result


def resolve_target(target: str) -> str:
    """
    Resolve hostname to IP address.

    Args:
        target: Hostname or IP address

    Returns:
        IP address string
    """
    try:
        # Check if it's already an IP address
        socket.inet_aton(target)
        return target
    except socket.error:
        # Try to resolve hostname
        try:
            ip = socket.gethostbyname(target)
            return ip
        except socket.gaierror:
            raise ValueError(f"Cannot resolve target: {target}")


def print_banner(target: str, ip: str, port_count: int, scan_type: str):
    """Print scan information header."""
    print("=" * 60)
    print(f"Port Scanner - Scan Report")
    print("=" * 60)
    print(f"Target:      {target} ({ip})")
    print(f"Ports:       {port_count}")
    print(f"Scan Type:   {scan_type}")
    print(f"Start Time:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)


def print_summary(open_ports: list, elapsed_time: float):
    """Print scan results summary."""
    print("\n" + "=" * 60)
    print(f"Scan Complete - Found {len(open_ports)} open port(s)")
    print(f"Duration: {elapsed_time:.2f} seconds")
    print("=" * 60)

    if open_ports:
        print(f"\n{'PORT':<10}{'STATUS':<10}{'SERVICE':<15}")
        print("-" * 35)
        for entry in open_ports:
            print(f"{entry['port']:<10}{entry['status']:<10}{entry['service']:<15}")


def sequential_scan(target: str, ports: list, timeout: float) -> list:
    """Scan ports one at a time (simplest approach for learning)."""
    open_ports = []
    for i, port in enumerate(ports):
        result = scan_port(target, port, timeout)
        if result["status"] == "open":
            open_ports.append(result)
        # Progress indicator
        progress = ((i + 1) / len(ports)) * 100
        print(f"\rScanning... {progress:.1f}% ({i + 1}/{len(ports)})", end="")
    return open_ports


def threaded_scan(target: str, ports: list, timeout: float, max_threads: int) -> list:
    """Scan ports using multiple threads for faster results."""
    open_ports = []
    completed = 0

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all scan jobs
        future_to_port = {
            executor.submit(scan_port, target, port, timeout): port
            for port in ports
        }

        # Collect results as they complete
        for future in as_completed(future_to_port):
            completed += 1
            result = future.result()
            if result["status"] == "open":
                open_ports.append(result)

            # Progress indicator
            progress = (completed / len(ports)) * 100
            print(f"\rScanning... {progress:.1f}% ({completed}/{len(ports)})", end="")

    return open_ports


def parse_port_range(port_str: str) -> list:
    """
    Parse port range string into list of ports.

    Supports formats:
    - Single port: "80"
    - Comma-separated: "22,80,443"
    - Range: "1-1000"
    - Mixed: "22,80,443,1000-1010"
    """
    ports = set()

    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))

    return sorted(ports)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="TCP Port Scanner - Educational Cybersecurity Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.1              Scan common ports
  python port_scanner.py example.com -p 1-1000    Scan ports 1-1000
  python port_scanner.py 10.0.0.1 --quick         Use quick preset
  python port_scanner.py 192.168.1.1 -t 50        Use 50 threads

Security Notice: Only scan targets you own or have permission to test.
        """
    )

    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="common",
                        help="Port range: 'common', 'all', or 'start-end' (e.g., 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=10,
                        help="Number of concurrent threads (default: 10)")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--quick", action="store_true",
                        help="Scan only the most common 20 ports")

    args = parser.parse_args()

    # Validate and resolve target
    try:
        target_ip = resolve_target(args.target)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Determine ports to scan
    if args.quick:
        ports = COMMON_PORTS[:20]  # Top 20 ports
        scan_type = "Quick (Top 20)"
    elif args.ports.lower() == "common":
        ports = COMMON_PORTS
        scan_type = "Common Ports"
    elif args.ports.lower() == "all":
        ports = list(range(1, 65536))
        scan_type = "All Ports (1-65535)"
    else:
        ports = parse_port_range(args.ports)
        scan_type = f"Custom ({args.ports})"

    # Run scan
    print_banner(args.target, target_ip, len(ports), scan_type)
    print("\nScanning...")

    start_time = time.time()

    if args.threads > 1:
        open_ports = threaded_scan(args.target, ports, args.timeout, args.threads)
    else:
        open_ports = sequential_scan(args.target, ports, args.timeout)

    elapsed_time = time.time() - start_time

    # Display results
    print()  # New line after progress
    print_summary(open_ports, elapsed_time)

    return 0


if __name__ == "__main__":
    exit(main())
