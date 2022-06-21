import socket

PORT = 5055
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDR)
msg = "screenshot('192.168.1.26', 59110)".encode()
msg += b' ' * (2048-len(msg))
sock.send(msg)
