import time
import socket


HOSTNAME="127.0.0.1"
PORT_SOCKET=9094
URL_TO_GO="www.baidu.com"

print('start client')



def after_tcp_connection(tls_socket):
  header = f"GET / HTTP/1.1\r\nHost: {URL_TO_GO}\r\n\r\n"
  print('sending http header to server_proxy')
  tls_socket.send(header.encode()) ## thats like b'. string to bytes.
  

def open_tcp_connection_with_outside_world(socket):
  header = (
    f"CONNECT {URL_TO_GO}:443 HTTP/1.1\r\n"
    f"Host: {URL_TO_GO}:443\r\n"
    "\r\n"
)
  s.send(header.encode()) 



# myself
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 6001))
# now connect to the web server on port 80 - the normal http port
s.connect((HOSTNAME, PORT_SOCKET))

import ssl



##

print('Gonna send msg')
time.sleep(1)

open_tcp_connection_with_outside_world(s)
raw_data_open_connection  = s.recv(4096)
if b"200 Connection Established" in raw_data_open_connection:
  context = ssl.create_default_context()
  tls_socket = context.wrap_socket(s, server_hostname=URL_TO_GO)
  after_tcp_connection(tls_socket)
else:
  print('we stopr')
  raise Exception("Tunnel not established")
## 

# We receive the data from the server_proxy
response = b""
while True:
    print('receiving data from server_proxy')
    raw_data_from_server_proxy  = tls_socket.recv(4096)
    response += raw_data_from_server_proxy
    if not raw_data_from_server_proxy:
        break
    print(raw_data_from_server_proxy.decode(),'DATA from server')
    with open("received.html", "wb") as f: f.write(response)
tls_socket.close()
with open("received.html", "wb") as f: f.write(response)


print('Sleep before dying')
time.sleep(3)