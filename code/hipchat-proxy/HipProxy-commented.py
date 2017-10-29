# listen on 127.0.0.1:5222
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 5222

# send everything to hipchatserver.com:5222
REMOTE_HOST = "10.11.1.25"  # hipchatserver.com
REMOTE_PORT = 5222

# buffer size in bytes
# we will need such a large buffer because server will send a lot of data after the connection is established
BUF_SIZE = 8192

import socket
import ssl
from binascii import hexlify, unhexlify

# create socket 127.0.0.1:5222

#  this can't be non-blocking for obvious reasons
listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind it to 127.0.0.1:5222
listensocket.bind((PROXY_HOST, PROXY_PORT))
listensocket.listen(1)  # 1 for now - you can add more if you want multiple clients but we only need one

print "\n[+] Created socket on %s:%s and listening" % (PROXY_HOST, PROXY_PORT)

# now accept connections from hipchat client
clientsocket, clientaddress = listensocket.accept()

# this should be localhost or 127.0.0.1
# str is needed because otherwise it cannot be printed properly and we get an errors
print "\n[+] Accepted connection from %s" % str(clientaddress)

# listen for xmpp_msg1 (first step of XMPP  handshake)
xmpp_msg1 = clientsocket.recv(BUF_SIZE)
print "\n[+] Received msg from client:\n%s" % (xmpp_msg1)

# create a connection to srver and send it
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect( (REMOTE_HOST, REMOTE_PORT) )
print "\n[+] Connected to server at %s:%s\n" % (REMOTE_HOST, REMOTE_PORT)

# send xmpp_msg1
serversocket.sendall(xmpp_msg1)
print "\n[+] Sending xmpp_msg1 to server"

# receive xmpp_msg2 from server
xmpp_msg2 = serversocket.recv(BUF_SIZE)
print "\n[+] Received msg from server:\n%s" %(xmpp_msg2)

# relay it to client
clientsocket.sendall(xmpp_msg2)
print "\n[+] Send xmpp_msg2 to client"

# receive xmpp_msg3
xmpp_msg3 = clientsocket.recv(BUF_SIZE)
print "\n[+] Received xmpp_msg3 (STARTTLS) from client:\n%s" % (xmpp_msg3)

# this should be the STARTTLS one
# <starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>

# relay it to server
serversocket.sendall(xmpp_msg3)
print "\n[+] Sent xmpp_msg3 (STARTTLS) to server"

# receive xmpp_msg4 from server
xmpp_msg4 = serversocket.recv(BUF_SIZE)
print "\n[+] Received xmpp_msg4 (PROCEED) from server:\n%s" %(xmpp_msg4)

# this should be PROCEED
# <proceed xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>

if "proceed" not in xmpp_msg4:
    print "\n [+] Something went wrong, server did not respond with proceed"
    exit()

else:
    clientsocket.sendall(xmpp_msg4)
    print "\n[+] Sending xmpp_msg4 (PROCEED) to client"

print "\n[+] Going TLS"

# now we must wrap our sockets in TLS
# fortunately this is very easy in Python

# converting clientsocket to TLS
# modify the path host.crt and host.key (if they are not in the same directory)
tlsclient = ssl.wrap_socket(clientsocket, keyfile="host.key", certfile="host.crt", server_side=True, cert_reqs=ssl.CERT_NONE)

# set it to non-blocking
tlsclient.setblocking(0)

# set timeout to 0.5 sec
tlsclient.settimeout(0.5)

# ssl.CERT_NONE == cert is not required and will not be validated if provided
# this is not generally safe but we know the endpoint in this scenario
# this means, don't care if hipchatserver.com responds with a crappy certificate
tlsserver = ssl.wrap_socket(serversocket, server_side=False, cert_reqs=ssl.CERT_NONE)
tlsserver.setblocking(0)
tlsserver.settimeout(0.5)

# SSL added and removed here :^)
# 2meta4me

# now we are going to juggle connections
# listen on one for half a second and send on the other one then vice versa

while 1:
    try:
        # receive on client-side
        msg_from_client = tlsclient.recv(BUF_SIZE)
        print ( "\n[+] Received from client:\n%s" % str(msg_from_client) )

        tlsserver.sendall(msg_from_client)

	# sockets are non-blocking which means that they will timeout
	# here we check if they actually timedout
    except socket.error as socket_exception:
        if "timed out" not in str(socket_exception):
            print "\n[+] Error receiving data from client\n%s" % str(socket_exception)

    try:
        msg_from_server = tlsserver.recv(BUF_SIZE)
        print( "\n[+] Received from server:\n%s" % str(msg_from_server) )
		
        tlsclient.sendall(msg_from_server)

    except socket.error as socket_exception:
         if "timed out" not in str(socket_exception):
            print "\n[+] Error receiving data from server\n%s" % str(socket_exception)
