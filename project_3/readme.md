
sudo python3 middleman.py


sudo python3 connect_http.py



https://chatgpt.com/g/g-p-6896efd10a848191adabe5f499dcfeb5-romain-schooling/c/69a00b93-7ae8-8326-94d8-ee884ebca9a5



# Instal stuff
pip3 install requests


# Creer un tun


Oui. ✅
On commence proprement.

---

# 🎯 Étape 1 — Créer tun0

D’abord assure-toi que le module TUN est chargé :

```bash
modprobe tun
```

---

Puis créer l’interface :

```bash
ip tuntap add dev tun0 mode tun
```

---

Puis lui donner une IP (exemple côté “client”) :

```bash
ip addr add 10.8.0.1/24 dev tun0
```

---

Puis l’activer :

```bash
ip link set tun0 up
```

---

# 🔎 Vérifier

```bash
ip a | grep tun0 -A2
```

Tu dois voir :

* tun0
* state UP
* 10.8.0.1/24

---

⚠️ On ne change PAS encore la default route.

---

Dis-moi si tun0 est bien UP.





make sure 
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000
is still workign with current tun i just made