# wireshark filter: tcp.port == 9094 or tcp.port == 80
# tcp.port == 9094 or ip.addr == 180.101.49.44
# ip.addr==153.3.238.127
import re
import select
import socket
import os
import base64
import hashlib
import time

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



def decode_websocket_frame(frame):
    byte0 = frame[0]
    byte1 = frame[1]

    fin = (byte0 >> 7) & 1
    rsv = (byte0 >> 4) & 0b111
    opcode = byte0 & 0x0F

    mask = (byte1 >> 7) & 1
    payload_len = byte1 & 0b01111111
    index = 2

    # extended payload length
    if payload_len == 126:
        payload_len = int.from_bytes(frame[index:index+2], "big")
        index += 2
    elif payload_len == 127:
        payload_len = int.from_bytes(frame[index:index+8], "big")
        index += 8

    masking_key = None
    if mask:
        masking_key = frame[index:index+4]
        index += 4

    masked_payload = frame[index:index+payload_len]

    if mask:
        payload_bytes = bytes(
            b ^ masking_key[i % 4] for i, b in enumerate(masked_payload)
        )
    else:
        payload_bytes = masked_payload

    try:
        payload_text = payload_bytes.decode("utf-8")
    except:
        payload_text = None

    return {
        "fin": fin,
        "rsv": rsv,
        "opcode": opcode,
        "mask": mask,
        "payload_length": payload_len,
        "masking_key": masking_key.hex() if masking_key else None,
        "payload_text": payload_text,
        "payload_bytes": payload_bytes.hex()
    }

def send_text_message(conn, text):
    print('gonna send text message')
    payload = text.encode("utf-8")
    length = len(payload)

    # FIN=1 + opcode=1 (text)
    first_byte = 0x81

    if length < 126:
        header = bytes([first_byte, length])
    elif length < 65536:
        header = bytes([first_byte, 126]) + length.to_bytes(2, "big")
    else:
        header = bytes([first_byte, 127]) + length.to_bytes(8, "big")

    frame = header + payload
    conn.sendall(frame)
    print('sent text message')

def send_pong_response(conn):
    response = b"\x8A\x00"   # FIN=1, Opcode=0xA (PONG), length=0
    print("send pong response")
    conn.sendall(response)


def handleWebSocketOnGoingConnection(conn):
    send_interval = 5  # seconds
    while True:
      # Wait up to send_interval seconds for client data (non-blocking wait)
      readable, _, _ = select.select([conn], [], [], send_interval)
      if readable:
        data = conn.recv(4096)
        if data:
          websocket_frame = decode_websocket_frame(data)
          print(websocket_frame, 'websocket_frame')
          print(websocket_frame['payload_text'], 'websocket_frame payload_text')
        else:
          print('no data received')
          break  # connection closed

      # Send server messages every loop (either after timeout or after handling client msg)
      print('gonna send pong response')
      send_pong_response(conn)
      print('sent pong response')
      send_text_message(conn, 'A test from the server')


      
def handleWebSocketNewConnection(conn, decoded):
  def make_magic_string(decoded):
      sec_webSocket_key = re.search(r"^Sec-WebSocket-Key:\s*([^\r\n]+)", decoded, re.MULTILINE).group(1)
      KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
      hash_object = hashlib.sha1((sec_webSocket_key + KEY).encode())
      return base64.b64encode(hash_object.digest())
  response = (
              b"HTTP/1.1 101 Switching Protocols\r\n"
              b"Upgrade: websocket\r\n"
              b"Connection: Upgrade\r\n"
              b"Sec-WebSocket-Accept: " + make_magic_string(decoded) + b"\r\n"
              b"\r\n"
          )
  print(response,'RESPONSE HERE SOCKET')
  return response

def extract_request(http_text):
    lines = http_text.split("\r\n")
    request_line = lines[0]

    # Méthode + chemin + version
    m = re.match(r"(\w+)\s+([^\s]+)\s+HTTP/[\d.]+", request_line)
    method, path = (m.group(1), m.group(2)) if m else (None, None)

    # Host
    m = re.search(r"^Host:\s*([^\r\n]+)", http_text, re.MULTILINE)
    connection = re.search(r"^Connection:\s*([^\r\n]+)", http_text, re.MULTILINE)
    connection = connection.group(1) if connection else None
    host = m.group(1) if m else None
    protocol = re.search(r"^Sec-WebSocket-Protocol:\s*([^\r\n]+)", http_text, re.MULTILINE)
    protocol = protocol.group(1) if protocol else None
    print(host, method, path, connection,'ALL received')
    return {
        "host": host,
        "method_name": method,
        "file_path": path,
        "connection":connection,
        "protocol":protocol
    }




while (True):
  conn, addr = s.accept()
  ##conn, addr = s.accept()  kill that one too
  raw_data = conn.recv(1024)
  print('ON?')

  print("Connexion acceptée depuis :", addr)
  decoded= raw_data.decode()
  json_data = extract_request(decoded)
  file_path = json_data['file_path']
  method_name = json_data['method_name']
  host = json_data['host']
  connection = json_data['connection']
  protocol = json_data['protocol']
  print(protocol,'PROTOCOL TEST HERE')
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
  print(connection,'connection TEST HERE')
  ## We check whether thats a socket connection
  if connection == "Upgrade":
    print('UPGRADE ISNT?')
    try:
      response =handleWebSocketNewConnection(conn, decoded)
      print(response,'RESPONSE HERE SOCKET to send')
      conn.sendall(response)
      handleWebSocketOnGoingConnection(conn)
    except Exception as e:
      print(e,'ERROR HERE')
      conn.sendall(
          b"HTTP/1.1 500 Internal Server Error\r\n"
          b"Content-Length: 0\r\n\r\n"
      )
      conn.close()
    #finally:
      ## conn.close() ## we DO NOT close the connexion. we want to re-use the TCP connection. 
      ## thats the main point of web-socket here
  # Wecheck whether thats a HTTP connection
  elif method_name == "GET" and connection != "Upgrade":
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
          conn.close()

      except FileNotFoundError:
          conn.sendall(
              b"HTTP/1.1 404 Not Found\r\n"
              b"Content-Length: 0\r\n\r\n"
          )
          conn.close()
  else:
      conn.sendall(
          b"HTTP/1.1 405 Method Not Allowed\r\n"
          b"Content-Length: 0\r\n\r\n"
      )
      conn.close()
  
      
  #s.sendto(outside_data, client_addr)



  #conn.close()




""" TO DO

  Votre serveur doit-être capable d'envoyer à intervalle régulier des frames « ping » (par exemple toutes les 30 secondes).
Vérifiez la réception du « pong » par le serveur. On veut observer dans la trace du serveur le délai entre l'émission du « ping » et la réception du « pong » correctement formaté. """