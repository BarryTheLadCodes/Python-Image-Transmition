import cv2, socket
import numpy as np
import base64
import keyboard
import pyautogui
import threading

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
message = b'Hello'

client_socket.sendto(message,(host_ip,port))

def sendMessages(message):
    client_socket.sendto(message,(host_ip,port))
    while True:
        keyboard.wait(' ')
        pos = pyautogui.position()
        if pos[0] > 441 and pos[0] < 941:
            if pos[1] > 165 and pos[1] < 665:
                message = f"{pos[0]-442} {pos[1]-166}"
                client_socket.sendto(message.encode('utf-8'),(host_ip,port))

thread = threading.Thread(target=sendMessages, args=(message, ))
thread.start()

while True:
    packet,_ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet,' /')
    npdata = np.frombuffer(data,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    cv2.imshow("RECEIVING VIDEO",frame)
    cv2.moveWindow("RECEIVING VIDEO",round(1366/2-250),round(768/2-250))
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        client_socket.close()
        break
