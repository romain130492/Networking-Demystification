# wireshark filter: tcp.port == 9094 or tcp.port == 80
# tcp.port == 9094 or ip.addr == 180.101.49.44

import re
import socket

print('start file')

# créer socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# côté serveur
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 9094))
s.listen(1)

def extract_hostname(http_text):
  m = re.search(r"^Host:\s*([^\r\n]+)", http_text, re.MULTILINE)
  host = m.group(1) if m else None
  return host


def create_socket_to_outside(host_to_go, port=80):
  socket_outside = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_outside.connect((host_to_go, port))
  return socket_outside


while (True):
  conn, addr = s.accept()
  print('ON?')
  print()

  print("Connexion acceptée depuis :", addr)

  raw_data = conn.recv(1024)
  host_to_go = extract_hostname(raw_data.decode())

  print(host_to_go,'HOST_TO_GO')
  if host_to_go:
    # we send the client payload to the targeted host. without touching it.
    socket_outside = create_socket_to_outside(host_to_go)
    print('created socket to:', host_to_go)
    socket_outside.send(raw_data)
    while True:
        data = socket_outside.recv(4096)
        if not data:
            break
        conn.send(data)
    socket_outside.close()

  else:
    print('NO HOST to GO TO. We are useless, we abort and die.')

  conn.close()