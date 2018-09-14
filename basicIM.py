import socket, sys, select, argparse
# Elaina Teramoto
# Network security 
# ert35

#parse the command line requirements
#-s: server, -p: port, -c: client
parser = argparse.ArgumentParser()
parser.add_argument("-s", dest = "server", action = 'store_true', default = False)
parser.add_argument("-p", dest = "port", default = 9896, type = int)
parser.add_argument("-c", dest = "client")
args = parser.parse_args()

#Default
HOST = ''
PORT = args.port

#the IM that deals with the sending and receiving 
def sendAndPrint(connect):
	# uses sys.stdout and sys.stin to handle the command line input and output
	sendAndPrint_list = [sys.stdin, connect]

	while 1: 
		reading, writable, exceptional = select.select(sendAndPrint_list, [], [], 0.0)
		for read in reading:
			if read == connect:
				data = connect.recv(1024)
				if data:
					sys.stdout.write(data)
					sys.stdout.flush()
				else:
					break
			else:
				message = sys.stdin.readline()
				if len(message) > 0:
					connect.send(message)

def server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen(1)
	conn, addr = server_socket.accept()
	try:
		sendAndPrint(conn)
	except KeyboardInterrupt:
		server_socket.close()

def client():
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((HOST, PORT))
	try:
		sendAndPrint(client_socket)
	except KeyboardInterrupt:
		client_socket.close()

if __name__ == '__main__':
	if (args.server == True):
		server()
	else:
		client()
