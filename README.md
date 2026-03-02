# Networking Demystification

Simple hands-on networking projects designed to deeply understand core concepts using **Python** and **Wireshark**.

Related to [RSX-102 course, CNAM](https://www.cnam.fr/formation/logiciels-outils-applications-services/technologies-pour-les-applications-en-reseau-contribution-au-profil-netdevops)


## Projects

### 1. TCP Proxy (Layer 4 – Transport)

A basic TCP proxy built in Python to understand:

* Socket programming
* Connection handling
* Bidirectional forwarding
* HTTP over TCP behavior

---

### 2. UDP Tunnel (Encapsulation – Layer 4)

A custom UDP tunneling mechanism to explore:

* Packet encapsulation
* Stateless transport
* NAT traversal concepts
* Reliability trade-offs

---

### 3. VPN (Layer 3 – TUN Interface)

A minimal VPN built using a TUN interface to understand:

* Layer 3 packet routing
* IP forwarding
* Virtual interfaces
* Traffic redirection









---------






ssh root@209.38.139.107 "tcpdump -i any -U -w -" | wireshark -k -i -

https://chatgpt.com/g/g-p-6896efd10a848191adabe5f499dcfeb5-romain-schooling/c/69a00b93-7ae8-8326-94d8-ee884ebca9a5