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
  s.sendto(make_http_header().encode(), (HOSTNAME, PORT_SOCKET))

  


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 6001))
# now connect to the web server on port 80 - the normal http port
#s.connect((HOSTNAME, PORT_SOCKET)) ## we kill that. we dont have a conneciton with UDP 
print('Gonna send msg')
time.sleep(1)
send_http_header()


s.settimeout(10)
response = b""

while True:
    try:
        data, addr  = s.recvfrom(4096)
        response += data ## tmp, but thats bad. cuz UDP will probably give packet not in the right order when its fragmented
    except socket.timeout:
        break


with open("received.html", "wb") as f: f.write(response)

#data, addr = s.recvfrom(4096)
#raw_data = data.decode()
#print(data,addr)
#print(raw_data,'raw_data')

print('Sleep before dying')
time.sleep(3)