import socket
import select
import re
import errno


def main():	

	host = "127.0.0.1"
	port = 54581
	address = host,port
	
	try:
		listenerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listenerSocket.bind((host,port))
		listenerSocket.listen(2)
	except socket.error as err:
		if err.errno == errno.EADDRINUSE:
			print "Socket in use, retrying"
			listenerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			listenerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			listenerSocket.bind((host,port))
			listenerSocket.listen(2)
		else:
			raise err




	connection, address = listenerSocket.accept()
	while 1:
		data = connection.recv(1024)
		print data.upper().rstrip()
		if re.search("exit",data):
			break

	connection.shutdown(socket.SHUT_RDWR)
	connection.close()


if __name__ == "__main__":
	main()