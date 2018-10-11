import socket, sys, select, argparse
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
# Elaina Teramoto
# Network security 
# ert35

# encrypt messages using AES-256 in CBC mode 
# use HMAC (hash function with a secret key) with SHA 256 for message authentication
#IVs are generated randomly	


#parse the command line requirements
#-s: server, -p: port, -c: client
parser = argparse.ArgumentParser()
parser.add_argument("-s", dest = "server", action = 'store_true', default = False)
parser.add_argument("-p", dest = "port", default = 9896, type = int)
parser.add_argument("-c", dest = "client")
parser.add_argument("--confkey", dest = "config")
parser.add_argument("--authkey", dest = "authen")

args = parser.parse_args()

#Default
HOST = ''
PORT = args.port
#aes block size is 16

def createHMAC():
	return HMAC.new(SHA256.new(args.authen).hexdigest(), digestmod = SHA256).hexdigest()
def createKey(sKey):
	return (SHA256.new(sKey).hexdigest())[:16]
def otpad(s):
	return s + (16 - len(s) % 16) * chr((16 - len(s) % 16))
def otUnpad(data):
	return data[0:-ord(data[-1])]


def encrypt(sKey, data):
	# 1. create a key using the configk key and create a random IV
	# 2. create hmac using the authKey 
	# 3. using the key, create an encrypt object
	# 4. create a pad and encrypt the plaintext using the pad and hmac
	# 5. return ciphertext and iv

	#1
	key = createKey(sKey)
	iv = Random.new().read(16)
	#2 
	hGen = createHMAC()
	#3
	eObject = AES.new(key, AES.MODE_CBC, iv)
	#4 
	pad = otpad(data)
	print(pad)
	ciphertext = eObject.encrypt(pad + hGen)
	#5
	return iv + ciphertext


def decrypt(sKey, data):
	# 1. take the iv from what was sent and hash 
	# 2. create hmac
	# 3. decrypt with iv and configKey
	# 4. check if hmac is correct, otherwise end
	#1
	key = createKey(sKey)
	iv = data[:16]
	#2
	newHash = createHMAC()[:64]
	#3

	dObject = AES.new(key, AES.MODE_CBC, iv)
	dMessage = dObject.decrypt(data[16:])

	dMes = dMessage[:64]
	#print("dMES")
	#print (dMes)
	#print("this is the new hasj")
	#print (newHash)
	padSize = (16 - (len(data) % 16))
	print(padSize)
	dMesi = dMessage[padSize:]
	#print(dMesi)
	newHash = newHash[:64-padSize]
	rint(newHash)

	#4
	if (newHash == dMesi):
		#print ("message was printed")
		#print (dMes)
		#print("I am confused")
		#print(dMes[:padSize])
		#print(otpad(dMes))
		#print("otUnpad")
		#print(otUnpad(dMes[:padSize]))
		return otUnpad(dMes[:padSize])

		#return message[0:-ord(message[-1])]
	else:
		sys.stdout.write("HMAC did not pass. Sorry!")
		sys.exit(0)



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
					sys.stdout.write(decrypt(args.config, data))
					sys.stdout.flush()
				else:
					break
			else:
				message = sys.stdin.readline()
				if len(message) > 0:
					connect.send(encrypt(args.config, message))

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
	if not args.config or not args.authen:
		print("please include the config key and authenication key")
	if (args.server == True):
		server()
	else:
		client()
