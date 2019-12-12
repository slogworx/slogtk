from scapy.all import IP, TCP, sr, conf
from random import randint
import sys


def pscan(host):
    conf.verb = False  # Silence the verbosity
    packet = IP(dst=host)/TCP(flags="S", sport=randint(6001, 6999), dport=(20, 1056))
    answer, no_answer = sr(packet, timeout=10)
    no_answer_ports, open_ports, closed_ports = [], [], []

    for ans in answer:
        for a in ans:
            flag = a.getlayer(TCP).flags
            if a.sport <= 1056:
                if flag == 'SA':  # Received SYN/ACK from port
                    open_ports.append(a.sport)
                elif flag == 'RA':  # Received RST/ACK from port
                    closed_ports.append(a.sport)

    for noa in no_answer:
        for n in noa:
            flag = n.getlayer(TCP).flags
            if not n.sport <= 1056:
                if flag == 'S':  # Received no response
                    no_answer_ports.append(n.dport)

    return open_ports, closed_ports, no_answer_ports


if __name__ == "__main__":
    if not (len(sys.argv) == 2):
        print(f"usage: {sys.argv[0]} target_address")
    else:
        answer, no_answer = [], []
        try:
            open_ports, closed_ports, no_answer_ports = pscan(sys.argv[1])
        except OSError as e:
            print(f'Invalid host: {e}')

    print(f'closed ports: {closed_ports}\n')
    print(f'open ports: {open_ports}\n')
    print(f'no answer ports: {no_answer_ports}\n')
