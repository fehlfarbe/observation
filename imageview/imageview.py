'''
Created on 13.08.2015

@author: kolbe
'''
import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = 'localhost'
TCP_PORT = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

while True:
    length = recvall(conn,16)
    if length is None:
        continue
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    #s.close()
    
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)
    cv2.waitKey(1)
cv2.destroyAllWindows() 

