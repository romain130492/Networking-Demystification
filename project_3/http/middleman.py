print('test middleman')



# middleman.py
import os
import fcntl
import struct

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

def open_tun(name="tun0"):
    tun = os.open("/dev/net/tun", os.O_RDWR)
    ifr = struct.pack("16sH", name.encode(), IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    return tun

def main():
    tun = open_tun("tun0")
    print("Listening on tun0 ...")

    while True:
        packet = os.read(tun, 2048)
        print(f"\nPacket length: {len(packet)} bytes")
        print(packet[:40])  # affiche les premiers bytes
        version = packet[0] >> 4
        print("IP version:", version)

if __name__ == "__main__":
    main()