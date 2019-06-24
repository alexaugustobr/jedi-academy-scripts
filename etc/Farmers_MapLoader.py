#!/usr/bin/python2.7
import socket
import sys


#data = " ".join(sys.argv[1:])
print "\nMBII JKA CLI Admin, a map loader with cheats!"
print "\nMade by the Farmers Sons Family"

mapname=raw_input("\nInsert the map name and press ENTER to send: >> ")

cmd="devmap"
rcon_pwd=""

HOST, PORT = "localhost", 29071

data=("\xff\xff\xff\xffrcon %s %s %s" % (rcon_pwd, cmd,mapname))
#print "\nSent:     {}".format(data)

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(data + "\n", (HOST, PORT))
received = sock.recv(1024)
if "ShutdownGame:" in received:
	print "\nServer Response: Map is loading!"
	print "Good Game Farmer Sons!"
else:
	print "\nServer Response: {}".format(received[9:-1])



#data=("\xff\xff\xff\xffrcon %s status" % (rcon_pwd))
#sock.sendto(data + "\n", (HOST, PORT))
#received = sock.recv(1024)

#print "Server Response: {}".format(received)
raw_input("\nPress Enter to exit")
