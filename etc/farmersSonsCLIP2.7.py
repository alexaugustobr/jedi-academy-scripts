#!/usr/bin/python2.7 
import socket
import sys
import time
#104.248.252.37: 29075
FARM_SERVER = "localhost"
EVENT_SERVER = "localhost"

class Server:
	host = ""
	port = 0
	rconPassword = "rcon"
	name = ""
	serverPassword = ""
	id = 0
	cheats = False
	def __init__(self, id, host, port, rconPassword, name, serverPassword, cheats):
		self.rconPassword = rconPassword
		self.host = host
		self.port = port
		self.name = name
		self.id = id
		self.cheats = cheats

	def sendData(self, data):
		print(data)
		data = ("\xff\xff\xff\xffrcon %s" % (data))
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(data + "\n", (self.host, self.port))
		receivedData = sock.recv(1024)
		if "ShutdownGame:" in receivedData:
			print("\nServer Response: Map is loading!")
		else:
			print( "\nServer Response: {}".format(receivedData[9:-1]))

	def sendRconCmd(self, cmd, parameter):
		data = ("%s %s %s" % (self.rconPassword, cmd, parameter))
		self.sendData(data)

	def loadMap(self, mapname):
		self.sendRconCmd("map", mapname)

	def loadMapWithCheats(self, mapname):
		self.sendRconCmd("devmap", mapname)

	def enableCheats(self, mapname):
		self.sendRconCmd("devmap", mapname)

	def disableCheats(self, mapname):
		self.sendRconCmd("map", mapname)

	def loadMapChangeMode(self, mapname, mbmode):
		print "The server will reload the map twice"
		self.sendRconCmd("mbmode", mbmode)
		print "Changing the map and disabling cheats in 20 seconds"
		time.sleep(20)
		self.sendRconCmd("map", mapname)

	def loadMapChangeModeWCheats(self,mapname, mbmode):
		print "The server will reload the map twice"
		self.sendRconCmd("mbmode", mbmode)
		print "Changing the map and enabling cheats in 20 seconds"
		time.sleep(20)
		self.sendRconCmd("devmap", mapname)

	def sendMessage(self, msg):
		self.sendRconCmd("svsay", msg)




class Option:
	cmd = ""
	name = ""
	id = 0
	def __init__(self,cmd,name, id):
		self.cmd = cmd
		self.name = name
		self.id = id




"""menu"""
servers = []
options = []

def printModesList():
	print "Select the mode"
	print "\n\t0 - Open Mode \t1 - Semi-Authentic Mode\n\t2 - Full-Authentic Mode \n\t3 - Duel mode"

def sendOption(option, server):
	if option.cmd == "loadMapWithCheats":
		map = raw_input("\nInsert the map name:\n")
		server.loadMapWithCheats(map)
	if option.cmd == "loadMap":
		map = raw_input("\nInsert the map name:\n")
		server.loadMap(map)
	if option.cmd == "changeModeWCheats":
		printModesList()
		mbmode = raw_input("\nInsert the mode number:\n")
		map = raw_input("\nInsert the map name:\n")
		server.loadMapChangeModeWCheats(map, mbmode)
	if option.cmd == "changeMode":
		printModesList()
		mbmode = raw_input("\nInsert the mode number:\n")
		map = raw_input("\nInsert the map name:\n")
		server.loadMapChangeMode(map, mbmode)
	if option.cmd == "sendMessage":
		msg = raw_input("\nInsert the message:\n")
		server.sendMessage(msg)

def buildOptions():
	changeMapWCheats = Option("loadMapWithCheats","Change the map and enable cheats",1)
	changeMap = Option("loadMap", "Change the map and disable cheats",2)
	changeMode = Option("changeMode", "Change the map and mode and disable cheats", 3)
	changeModeWCheats = Option("changeModeWCheats", "Change the map and mode and enable cheats", 4)
	sendMessage = Option("sendMessage", "Send a message for the players", 5)
	options.append(changeMapWCheats)
	options.append(changeMap)
	options.append(changeMode)
	options.append(changeModeWCheats)
	options.append(sendMessage)
	#optionsList.append("3 - Change mbmode and enable cheats")
	#optionsList.append("4 - Change mbmode and disable cheats")

def findOptionsById(id):
	for option in options:
		if id == option.id:
			return option
	return None

def findServersById(id):
	for server in servers:
		if id == server.id:
			return server
	return None

def printServerList():
	for i in range(0, len(servers)):
		print "\t%d - %s" % (i + 1, servers[i].name)

def printOptionsList():
	for option in options:
		print "\t%d - %s" % (option.id, option.name)

def drawMenu():
	print "\nOptions list:"
	printOptionsList()
	optionNumber = int(raw_input("\nType a option number from the list:\n"))
	option = findOptionsById(optionNumber)
	if option!=None:
		print "\nSelect a server:"
		printServerList()
		serverNumber = int(raw_input("\nType the server number from the list:\n"))
		server = findServersById(serverNumber)
		if server!=None:
			sendOption(option,server)
		else:
			"Invalid server"
	else:
		print "Invalid option"

def buildServers():
	farm = Server(1,FARM_SERVER, 29070, "rcon", "The Farmer Sons Sever", "", True)
	servers.append(farm)

def main():
	print "\nMBII JKA CLI Admin"
	print "\nMade by the Farmers Sons Family (v2.1)"
	buildServers()
	buildOptions()
	while True:
		drawMenu()





"""main"""
main()
