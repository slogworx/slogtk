from scapy.all import IP, TCP, sr, conf
from random import randint
import sys


def pscan(host):
    conf.verb = False  # Silence the verbosity
    packet = IP(dst=host)/TCP(flags="S", sport=randint(6001, 6999), dport=(20, 1056))
    answer, no_answer = sr(packet, timeout=10)
    no_answer_ports, answer_ports = [], []
    for noa in no_answer:
        for n in noa:
            no_answer_ports.append(n.dport)

    for ans in answer:
        for a in ans:
            flag = a.getlayer(TCP).flags
            if flag == 'SA':
                answer_ports.append(a.sport)
    return answer_ports, no_answer_ports


if __name__ == "__main__":
    if not (len(sys.argv) == 2):
        print(f"usage: {sys.argv[0]} target_address")
    else:
        answer, no_answer = [], []
        try:
            answer, no_answer = pscan(sys.argv[1])
        except OSError as e:
            print(f'Invalid host: {e}')

    print(f'closed ports: {no_answer}\n')
    print(f'open ports: {answer}\n')
