import time
import socket
HOSTNAME="127.0.0.1"
PORT_SOCKET=9094
URL_TO_GO="http://google.com"

print('start client')

def send_test_msg():
  s.send(b"hello test")
  print('Sent msg')
  time.sleep(3)
  s.send(b"test2")

def make_http_header():
    header = f"GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n"
    return header

def send_http_header():
  print('sending http header to server_proxy')
  s.send(make_http_header().encode()) ## thats like b'. string to bytes.
  


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 6001))
# now connect to the web server on port 80 - the normal http port
s.connect((HOSTNAME, PORT_SOCKET))
print('Gonna send msg')
time.sleep(1)
send_http_header()
# We receive the data from the server_proxy
response = b""
while True:
    print('receiving data from server_proxy')
    raw_data_from_server_proxy  = s.recv(4096)
    response += raw_data_from_server_proxy
    if not raw_data_from_server_proxy:
        break
    print(raw_data_from_server_proxy.decode(),'DATA from server')
    with open("received.html", "wb") as f: f.write(response)
s.close()
with open("received.html", "wb") as f: f.write(response)


print('Sleep before dying')
time.sleep(3)