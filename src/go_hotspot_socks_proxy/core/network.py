import psutil
import socket
from dataclasses import dataclass
from typing import Optional
from rich.progress import Progress
from rich.console import Console

console = Console()

@dataclass
class NetworkInterface:
    name: str
    ip: str
    is_up: bool
    is_wireless: bool

def scan_interfaces() -> Optional[NetworkInterface]:
    """Scan for available network interfaces and return the most suitable one"""
    with Progress() as progress:
        task = progress.add_task("Scanning network interfaces...", total=1)
        
        # Get all network interfaces
        interfaces = []
        for name, addrs in psutil.net_if_addrs().items():
            # Skip loopback and virtual interfaces
            if name.startswith(('lo', 'vmnet', 'docker', 'veth')):
                continue
                
            # Get IPv4 address
            ipv4 = next((addr.address for addr in addrs 
                        if addr.family == socket.AF_INET), None)
            if not ipv4:
                continue
                
            # Check if interface is up
            stats = psutil.net_if_stats().get(name)
            if not stats or not stats.isup:
                continue
                
            # Determine if it's likely a wireless interface
            is_wireless = name.startswith(('wlan', 'wifi', 'en'))
            
            interfaces.append(NetworkInterface(
                name=name,
                ip=ipv4,
                is_up=True,
                is_wireless=is_wireless
            ))
        
        progress.update(task, advance=1)
        
        # Prefer wireless interfaces
        wireless = [iface for iface in interfaces if iface.is_wireless]
        if wireless:
            return wireless[0]
        elif interfaces:
            return interfaces[0]
        
        return None 