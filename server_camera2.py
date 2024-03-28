import cv2, socket
import numpy as np
import time
import base64
import threading
import time

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print(f'[LISTENING] Listening on {socket_address}')
vid = cv2.VideoCapture(0)

def recieveMessages():
    while True:
        msg = server_socket.recv(2048)
        if msg != b'Hello':
            msg = msg.decode('utf-8')
            coords = list(msg.split(" "))
            print(coords)
            
thread = threading.Thread(target=recieveMessages)
thread.start()

while True:
    msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
    print(f'[CONNECTION] New connection at {client_addr}')
    while(vid.isOpened()):
        _,frame = vid.read()
        frame = cv2.resize(frame,(500,500))
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        server_socket.sendto(message,client_addr)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            server_socket.close()
            break
