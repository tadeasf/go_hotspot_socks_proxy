import subprocess
import re
from rich.console import Console
from rich.table import Table
from prompt_toolkit.shortcuts import ProgressBar

console = Console()

def get_interface_info():
    with ProgressBar(title="Scanning network interfaces...") as pb:
        for _ in pb(range(1)):
            result = subprocess.run(['ifconfig', 'en0'], capture_output=True, text=True)
    
    output = result.stdout
    
    # Parse interface information
    ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
    mac_match = re.search(r'ether (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', output)
    status_match = re.search(r'status: (\w+)', output)
    
    return {
        'ip': ip_match.group(1) if ip_match else 'Not found',
        'mac': mac_match.group(1) if mac_match else 'Not found',
        'status': status_match.group(1) if status_match else 'Unknown'
    }

def show_wifi_info():
    info = get_interface_info()
    
    table = Table(title="WiFi Interface (en0) Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("IP Address", info['ip'])
    table.add_row("MAC Address", info['mac'])
    table.add_row("Status", info['status'])
    
    console.print(table)
    return info