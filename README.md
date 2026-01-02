Firewall Rule Generator
A Python-based firewall rule generator for both Windows and Linux. It allows users to quickly generate firewall commands without memorizing iptables or netsh syntax.

Features
Generates firewall rules for Windows (netsh) and Linux (iptables)

Supports Source IP, Destination IP, Port, Protocol, and Action (ACCEPT/DROP or ALLOW/BLOCK)

Handles optional fields (blank input defaults to "any")

User-friendly prompts for quick rule generation

Safe: does not apply rules automatically; only prints commands

Prerequisites
Python 3.6 or higher

ipaddress module (built-in with Python 3)

Installation
Clone or download the repository:

bash
Copy code
git clone <repo_url>
or download the ZIP and extract it.

Navigate to the project directory:

bash
Copy code
cd firewall-rule-generator
Usage
Run the script in your terminal or command prompt:

bash
Copy code
python firewall_rule_generator.py
Follow the prompts:

Source IP (CIDR) – Enter a specific IP or network (e.g., 192.168.1.10/32), or leave blank for any

Destination IP (CIDR) – Enter a specific IP or network, or leave blank for any

Port – Enter the port number (1–65535), or leave blank for any

Action – ACCEPT / DROP (Linux) or ALLOW / BLOCK (Windows)

Protocol – TCP, UDP, or any

After all inputs, the script will print the generated firewall commands:

nginx
Copy code
Linux iptables command:
iptables -A INPUT -p tcp -s 192.168.1.10 --dport 22 -j ACCEPT

Windows netsh command:
netsh advfirewall firewall add rule name=MyRule action=ALLOW protocol=TCP remoteip=192.168.1.10 localport=22
How to apply the rules
Linux: copy the iptables command and run as root:

bash
Copy code
sudo iptables -A INPUT -p tcp -s 192.168.1.10 --dport 22 -j ACCEPT
Windows: copy the netsh command and run in an Admin CMD:

cmd
Copy code
netsh advfirewall firewall add rule name="MyRule" action=ALLOW protocol=TCP remoteip=192.168.1.10 localport=22
Notes
Rule order matters in iptables: first match wins

Empty input for Source or Destination IP means any IP

Ports can be left blank for all ports

Only generates commands; does not apply them automatically

Example Workflow
yaml
Copy code
Source IP: 192.168.1.5
Destination IP: 
Port: 22
Action: ACCEPT
Protocol: TCP
Generates:

pgsql
Copy code
iptables -A INPUT -p tcp -s 192.168.1.5 --dport 22 -j ACCEPT
netsh advfirewall firewall add rule name=MyRule action=ALLOW protocol=TCP remoteip=192.168.1.5 localport=22
License
MIT License – free to use and modify.

