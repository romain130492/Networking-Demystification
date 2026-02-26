#tcp.port == 9094 or ip.addr == 180.101.51.73
import socket
import re

print("start file")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 9094))
s.listen(5)

def extract_host_and_port_connect(request_line):
    # CONNECT www.baidu.com:443 HTTP/1.1
    parts = request_line.split()
    host_port = parts[1]
    host, port = host_port.split(":")
    return host, int(port)

def extract_host_http(http_text):
    m = re.search(r"^Host:\s*([^\r\n]+)", http_text, re.MULTILINE)
    if not m:
        return None
    host = m.group(1)
    if ":" in host:
        host, port = host.split(":")
        return host, int(port)
    return host, 80

while True:
    conn, addr = s.accept()
    print("Connexion acceptée depuis :", addr)

    first_packet = conn.recv(4096)

    if not first_packet:
        conn.close()
        continue

    request_text = first_packet.decode(errors="ignore")

    # =========================
    # HTTPS CONNECT MODE
    # =========================

    first_line = request_text.split("\r\n")[0]
    host, port = extract_host_and_port_connect(first_line)

    print("CONNECT to:", host, port)

    socket_outside = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_outside.connect((host, port))

    # répondre au client que le tunnel est prêt
    conn.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")

    # tunnel simple bidirectionnel
    while True:
        try:
            data_from_client = conn.recv(4096)
            if data_from_client:
                socket_outside.sendall(data_from_client)

            data_from_server = socket_outside.recv(4096)
            if data_from_server:
                conn.sendall(data_from_server)

            if not data_from_client and not data_from_server:
                break

        except:
            break

    socket_outside.close()
    conn.close()
