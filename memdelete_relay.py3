#!/usr/bin/env python3

from socket import *
import threading
sock=socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 20)
sock.bind(('',11211))
sock.listen(5)

class ClientThread(threading.Thread):

	def __init__(self, ip, port, socket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		print("[+] New thread started for "+ip+":"+str(port))

	def run(self):
		while True:
			try:
				data=self.socket.recv(1024)
				
				if data == b'':
					print("client closed connection")
					self.socket.close()
					break

				print("'client sent us':",data.strip())
				self.socket.sendall(b'DELETED\n')

				# open socket to other server
				sock_clzdb = socket(AF_INET, SOCK_STREAM)
				sock_clzdb.connect(('server_address_here',11211))
				sock_clzdb.send(data) # send delete request
				print('server zei:', sock_clzdb.recv(1024).strip())
				sock_clzdb.close
			except:
				print("client closed connection")
				self.socket.close()

while True:
	(clientsock, (ip, port)) = sock.accept()
	newthread = ClientThread(ip, port, clientsock)
	newthread.start()

sock.close()
