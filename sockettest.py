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
			port = 23
	else:
		port = int(args.port)
	
	address = host,port
	mainSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mainSocket.connect((host,port))
	negotiation = False
	while mainSocket in select.select([mainSocket], [], [], 1)[0]:
  		line = mainSocket.recv(1024)
  		print line.encode("hex")
  		if line and not negotiation:
  			mainSocket.sendall("fffc18fffc20fffc23fffc27".decode("hex"))
  			negotiation = True



if __name__ == "__main__":
	main()