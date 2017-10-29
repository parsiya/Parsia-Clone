import socket, ssl
from binascii import hexlify, unhexlify
dump = open("everything.dump", "wb")
serverDump = open("fromserver.dump", "wb")
clientDump = open("fromclient.dump", "wb")
listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.bind(("127.0.0.1", 5222))
listensocket.listen(1)  # 1 for now - you can add more if you want multiple clients but we only need one
clientsocket, clientaddress = listensocket.accept()
xmpp_msg1 = clientsocket.recv(8192)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect( ("10.11.1.25", 5222) )
serversocket.sendall(xmpp_msg1)
xmpp_msg2 = serversocket.recv(8192)
clientsocket.sendall(xmpp_msg2)
xmpp_msg3 = clientsocket.recv(8192)
serversocket.sendall(xmpp_msg3)
xmpp_msg4 = serversocket.recv(8192)
tlsclient = ssl.wrap_socket(clientsocket, keyfile="host.key", certfile="host.crt", server_side=True, cert_reqs=ssl.CERT_NONE)
tlsclient.setblocking(0)
tlsclient.settimeout(0.5)
tlsserver = ssl.wrap_socket(serversocket, server_side=False, cert_reqs=ssl.CERT_NONE)
tlsserver.setblocking(0)
tlsserver.settimeout(0.5)
while 1:
    try:
        msg_from_client = tlsclient.recv(8192)
        dump.write ( "\n[+] Received from client:\n%s" % str(msg_from_client) )
        clientDump.write( str(msg_from_client)+"\n" )
        tlsserver.sendall(msg_from_client)
    except socket.error as socket_exception:
        if "timed out" not in str(socket_exception):
            print "\n[+] Error receiving data from client\n%s" % str(socket_exception)
    try:
        msg_from_server = tlsserver.recv(8192)
        dump.write( "\n[*] Received from server1:\n%s" % str(msg_from_server) )
        serverDump.write( str(msg_from_server)+"\n" )
        tlsclient.sendall(msg_from_server)
        clientDump.flush()
        serverDump.flush()
    except socket.error as socket_exception:
         if "timed out" not in str(socket_exception):
            print "\n[+] Error receiving data from server\n%s" % str(socket_exception)
