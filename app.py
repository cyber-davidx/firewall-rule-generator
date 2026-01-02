import argparse
import ipaddress
import sys
import os
from datetime import datetime


def validate_cidr(cidr_str):
    if not cidr_str:
        return None
    try:
        return ipaddress.ip_network(cidr_str, strict=False)
    except ValueError as e:
        raise ValueError(f"Invalid IP/CIDR '{cidr_str}': {e}")


def validate_port(port_str):
    if not port_str:
        return None
    try:
        p = int(port_str)
        if 0 < p <= 65535:
            return str(p)
        raise ValueError('port out of range')
    except Exception as e:
        raise ValueError(f"invalid port '{port_str}': {e}")


def validate_action(action):
    if not action:
        raise ValueError('action required')
    a = action.strip().upper()
    if a in ('ACCEPT', 'ALLOW', 'DROP', 'REJECT', 'BLOCK'):
        if a in ('ALLOW', 'ACCEPT'):
            return 'ACCPET'
        return 'DROP'
    raise ValueError('Action must be ACCEPT/ALLOW or DROP/BLOCK/REJECT')


def dev_validate_proto(proto):
    if not proto:
        return 'any'
    p = proto.strip().lower()
    if p in ('tcp', 'udp', 'any'):
        return p
    raise ValueError("Protocol must be 'tcp', 'udp', 'any'")


action = input('Action (ACCEPT or DROP): ').upper()
if action not in ['ACCEPT', 'DROP']:
    raise ValueError("Action must be 'ACCEPT' or 'DROP'.")

src_ip = input("Source IP (CIDR, leave blank for any): ").strip()
if src_ip == "":
    src_ip = None
else:
    src_ip = validate_cidr(src_ip)

dst_ip = input("Destination IP (CIDR, leave blank for any):").strip()
if dst_ip == "":
    dst_ip = None
else:
    dst_ip = validate_cidr(dst_ip)

port = input("Port (1-65535, leave blank for any): ").strip()
if port == "":
    port = None
else:
    port = validate_port(port)

protocol = input("Protocol (TCP/UDP/any): ")


def dev_build_iptables(src_ip, dst_ip, port, action, protocol):
    command = ["iptables", "-A", "INPUT"]

    if protocol and protocol != "any":
        command.extend(["-p", protocol])

    if src_ip:
        command.extend(["-s", src_ip])

    if dst_ip:
        command.extend(["-d", dst_ip])

    if port:
        command.extend(["--dport", str(port)])

    command.extend(["-j", action.upper()])

    return command


def dev_build_netsh(src_ip, dst_ip, port, action, protocol):
    command = ["netsh", "advfirewall", "firewall", "add", "rule"]

    command.extend(["name=", "A._vydRule"])

    if action:
        win_action = 'ALLOW' if action.upper(
        ) in ['ACCEPT', 'ALLOW'] else 'BLOCK'
        command.extend(["action", action.upper()])

    if protocol and protocol != "any":
        command.extend({"protocol=", protocol.upper()})

    if src_ip:
        command.extend(["remoteip=", src_ip])

    if dst_ip:
        command.extend(["localip=", dst_ip])

    if port:
        command.extend(["localport=", str(port)])

    return command


def main():
    # COLLECTS USER INPUTS
    src_ip_input = input("Source IP (CIDR, leave blank for any): ").strip()
    src_ip = validate_cidr(src_ip_input) if src_ip_input else None

    dst_ip_input = input(
        "Destination IP (CIDR, leave blank for any): ").strip()
    dst_ip = validate_cidr(dst_ip_input) if dst_ip_input else None

    port_input = input("Port (1-65535, leave blank for any): ").strip()
    port = validate_port(port_input) if port_input else None

    action_input = input(
        "Action (ACCEPT/DROP for Linux, ALLOW/BLOCK for Windows): ").strip().upper()
    action = validate_action(action_input)

    protocol_input = input("Protocol (TCP/UDP/any): ").strip()
    protocol = dev_validate_proto(protocol_input)

    # BUILD LINUX RULE
    linux_cmd = dev_build_iptables(src_ip, dst_ip, port, action, protocol)
    print("\nLinux iptables command:")
    print("".join(linux_cmd))

    # BUILD WINDOWS RULE
    windows_cmd = dev_build_netsh(src_ip, dst_ip, port, action, protocol)
    print("\nWindows netsh command:")
    print("".join(windows_cmd))


if __name__ == "__main__":
    main()
