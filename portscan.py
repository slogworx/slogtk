from scapy.all import IP, TCP, sr, conf
from random import randint
import sys


def pscan(host):
    # Silence the verbosity
    #conf.verb = False
    packet = IP(dst=host)/TCP(flags="S", sport=randint(6001, 6999), dport=(20, 1024))
    print('Probing ports 20 through 1024:\n')
    ans, noa = sr(packet, timeout=2)

    for a in ans:
        if not (a[1].sprintf("%TCP.flags%") == "RA"):
            print(f"Service open on port {a[1].sport}")


if __name__ == "__main__":
    if not (len(sys.argv) == 2):
        print(f"usage: {sys.argv[0]} target_address")
    else:
        pscan(sys.argv[1])
