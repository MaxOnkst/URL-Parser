# Author: Max Onkst
# 1/31/2022
import time
import socket

TIMEOUT = 10 # unit is seconds
BUF_SIZE = 1024 # unit is bytes

class TCPsocket:

    # Constructor: create an object
    def __init__(self):
        self.sock = None
        self.host = ""  # remote server's host name


    # create a TCP socket
    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    print("created a tcp socket!")
        except socket.error as e:
            print("Failed to create a TCP socket {}".format(e))
            self.sock = None


    # Return the ip of input hostname. Both ip and hostname in string
    def getIP(self, hostname):
        time1 = time.time()*1000
        self.host = hostname
        if (len(hostname) > 64):  # socket fails with idna codec error when a host name exceeds 64 characters.
            return None
        try:
            ip = socket.gethostbyname(hostname)   # ip is a local variable to getIP(hostname), ip is of string type
        except socket.gaierror:
            print("Failed to gethostbyname")
            return None
        time2 = time.time()*1000
        print("Doing DNS... done in", round(time2-time1), " ms, found", ip)
        return ip


    # connect to a remote server: IP address (a string), port (integer)
    def connect(self, ip, port):
        time1 = time.time()*1000
        if self.sock is None or ip is None:
            self.sock = None
            return
        try:
            self.sock.settimeout(TIMEOUT)
            self.sock.connect((ip, port))
            time2 = time.time()*1000
        except socket.error as e:
            print("Failed to connect: {}".format(e)) # if timeout, socket error in receive: timed out
            self.sock.close()
            self.sock = None

    # send request to server. Input request is a string, return the number of bytes sent
    def send(self, request): # request is a bytearray
        bytesSent = 0
        if self.sock is None:
            return 0
        try:
            bytesSent = self.sock.sendall(request) #.encode())   # encode(): convert string to bytes
        except socket.error as e:
            print("socket error in send: {}".format(e))
            self.sock.close()
            self.sock = None

        #print("Bytes sent: ", bytesSent)
        return bytesSent

    # Receive the response from the server. Return the reply as bytearray
    def receive(self) -> bytearray:

        reply = bytearray()
        if self.sock is None:
            return reply  # return an empty bytearray, terminate this method

        self.sock.settimeout(TIMEOUT) # Sets the socket to timeout after TIMEOUT seconds of no activity

        # else we have data to read
        bytesRecd = 0
        try:
            while True:     # use a loop to receive receive all data
                data = self.sock.recv(BUF_SIZE)  # returned chunk of data with max length BUF_SIZE. data is in bytes
                if data == b'':  # if empty bytes
                    break
                else:
                    reply += data  # append to reply
                    bytesRecd += len(data)
                    if (bytesRecd > 16000): # bigger than 16K bytes. Do not let remote server overload our RAM
                        break
        except socket.error as e:
            print("socket error in receive: {}".format(e))  # if timeout, socket error in receive: timed out
            self.sock.close()
            self.sock = None

        return reply, bytesRecd

    # Close socket
    def close(self):
        if not (self.sock is None):
            self.sock.close()