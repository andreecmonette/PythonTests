import socket
import re
import argparse
import select



def main():	
	parser = argparse.ArgumentParser()
	parser.add_argument("host")
	parser.add_argument("--port","-p")
	args = parser.parse_args()
	host = args.host
	if not args.port:
		portMatch = re.match("^(.*):(\d+)$", args.host)
		if portMatch:
			port = int(portMatch.group(2))
			host = portMatch.group(1)
		else:
			port = 80
	else:
		port = int(args.port)
	
	address = host,port
	mainSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mainSocket.connect((host,port))
	requested = False
	mainSocket.send("GET / HTTP/1.1\n")
	mainSocket.send("Host: "+host+"\n")
	mainSocket.send("\n")
	requested = True
	while True:
  		line = line + mainSocket.recv(256)
  	

if __name__ == "__main__":
	main()