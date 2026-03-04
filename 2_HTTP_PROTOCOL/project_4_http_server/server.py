# wireshark filter: tcp.port == 9094 or tcp.port == 80
# tcp.port == 9094 or ip.addr == 180.101.49.44
# ip.addr==153.3.238.127
import re
import socket
import os

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



def extract_request(http_text):
    lines = http_text.split("\r\n")
    request_line = lines[0]

    # Méthode + chemin + version
    m = re.match(r"(\w+)\s+([^\s]+)\s+HTTP/[\d.]+", request_line)
    method, path = (m.group(1), m.group(2)) if m else (None, None)

    # Host
    m = re.search(r"^Host:\s*([^\r\n]+)", http_text, re.MULTILINE)
    host = m.group(1) if m else None
    print(host, method, path,'TEST HEREwww')
    return {
        "host": host,
        "method_name": method,
        "file_path": path
    }


""" def create_socket_to_outside(host_to_go, port=80):
  socket_outside = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_outside.connect((host_to_go, port))
  return socket_outside """


while (True):
  conn, addr = s.accept()
  ##conn, addr = s.accept()  kill that one too
  raw_data = conn.recv(1024)
  print('ON?')

  print("Connexion acceptée depuis :", addr)

  json_data = extract_request(raw_data.decode())
  file_path = json_data['file_path']
  method_name = json_data['method_name']
  host = json_data['host']
  print(file_path, method_name, host,'TEST HERE')
  #file_path = "/Users/romain/Desktop/CNAM/RSX102/sec1-3-projects-gpt/project_4_http_server/index.html"

  # Dossier de base = dossier où tourne le serveur
  base_dir = os.getcwd()

  # Si on demande "/", on sert index.html
  if file_path == "/":
      file_path = "index.html"
  else:
      file_path = file_path.lstrip("/")  # enlever le "/" initial

  # Normalisation pour éviter ../
  safe_path = os.path.normpath(file_path)

  # Construire chemin complet
  full_path = os.path.join(base_dir, safe_path)

  if method_name == "GET":
      try:
          with open(full_path, "rb") as f:
              content = f.read()

          response = (
              b"HTTP/1.1 200 OK\r\n"
              b"Content-Type: text/html\r\n"
              b"custom: love_it_kill_it\r\n"
              b"Content-Length: " + str(len(content)).encode() + b"\r\n"
              b"\r\n" +
              content
          )

          conn.sendall(response)

      except FileNotFoundError:
          conn.sendall(
              b"HTTP/1.1 404 Not Found\r\n"
              b"Content-Length: 0\r\n\r\n"
          )
  else:
      conn.sendall(
          b"HTTP/1.1 405 Method Not Allowed\r\n"
          b"Content-Length: 0\r\n\r\n"
      )
      
  #s.sendto(outside_data, client_addr)
  conn.close()


  #conn.close()