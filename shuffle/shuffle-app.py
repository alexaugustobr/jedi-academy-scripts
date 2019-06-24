#!/usr/bin/python2.7

#(.[0-9]*:.[0-9]*) (.*[0-9]:) (say:) (.*:) ("![s|n|y|N|S|Y|0|1]")
# 30:04 0: say: ^2Tigao: "lol"
# 0:22 say: Server: lol say: dasdsad

# 35:52 ClientDisconnect: 0

#(?:intended)(.*)(?:to match)

import re
import datetime
import time
import os
import socket
import struct

SERVER_LOG_PATH = '/home/alex/.ja/MBII/server.log'

REGEX_SAY_COMMAND = r'(.[0-9]*:.[0-9]*) (.*[0-9]:) (say:) (.*:) ("!(shuffle|shufle|sh)")'

SERVER_RCON_PWD = 'rcon'
SERVER_IP = '127.0.1.1'
SERVER_PORT = 29070

MSG_ONLINE = 'Shuffle votation is on!'

MSG_VOTATION_PASS = 'Shuffle passed!'

MSG_VOTATION_FAIL = 'Shuffle failed!'

MSG_VOTATION_INITIALIZED = 'Shuffle votation initialized!'

VOTATION_MAX_TIME_TO_FAIL = 5

MSG_PLATERS_WANTS = '{}/{} players wants to Shuffle!'

DEFAULT_MESSAGE_DECODER = 'iso-8859-1'

class Console:
	@staticmethod
	def info(message):
		finalMessage = '({}) INFO: {}'.format(datetime.datetime.now(), message)
		print(finalMessage)

class LogFile():
	def __init__(self, serverLogPath):
		self.serverLogPath = serverLogPath
		self._cached_stamp = 0

	def read(self):
		file = open(self.serverLogPath, 'r+')
		return file

	def isChanged(self):
		stamp = os.stat(self.serverLogPath).st_mtime
		if stamp != self._cached_stamp:
			self._cached_stamp = stamp
			return True
		else:
			return False

		
		
class VoteExtractor:

	def __init__(self, regex):
		self.regex = regex

	def extract(self, stringToExtract):
		result = re.search(self.regex, stringToExtract)

		if (not result):
			return None

		messageId = result.group(1).strip()
		playerId = result.group(2).strip()
		playerName = result.group(4).strip()
		optionMessage = result.group(5).strip()
		
		return Vote(messageId, playerId, playerName, optionMessage)

class Votation:

	voteDict = {}
	votes = 0
	totalPlayers = 0
	
	def addVote(self, vote):
		self.voteDict[vote.playerId] = vote

	def calculate(self):
		for key in self.voteDict.keys():
			vote = self.voteDict[key]
			votes = votes + 1

	def reset(self):
		self.voteDict = {}
		self.votes = 0
		self.totalPlayers = 0

	def isPassed(self):
		return self.votes > self.totalPlayers

	def __str__(self):
		strx = """
		votes = {}
		totalPlayers = {}
		isPassed = {}
		""".format(self.votes, self.totalPlayers, self.isPassed())
		return strx
		

class Vote:

	def __init__(self, messageId, playerId, playerName, optionMessage):
		self.messageId = messageId
		self.playerId = playerId
		self.playerName = playerName
		self.optionMessage = optionMessage 

	def __str__(self):

		strx = """
		messageId = {}
		playerId = {}
		playerName = {}
		optionMessage  = {}
		""".format(self.messageId, self.playerId, self.playerName, self.optionMessage)

		return strx

class Server:

	def __init__(self, host, port, rconPassword):
		self.rconPassword = rconPassword
		self.host = host
		self.port = port

	def sendData(self, data):
		data = ("\xff\xff\xff\xffrcon %s\n" % (data))
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(data, (self.host, self.port))
		receivedData = self.recv_timeout(sock)
		print(receivedData.decode(DEFAULT_MESSAGE_DECODER).strip())

	def sendRconCmdWithParameter(self, cmd, parameter):
		data = ("%s %s %s" % (self.rconPassword, cmd, parameter))
		self.sendData(data)

	def sendRconCmd(self, cmd):
		data = ("%s %s" % (self.rconPassword, cmd))
		self.sendData(data)

	def sendMessage(self, msg):
		self.sendRconCmdWithParameter("svsay", msg)

	def sendShuffle(self):
		self.sendRconCmd("shuffle")

	def requestStatus(self):
		self.sendRconCmd("status")

	def recv_timeout(self, the_socket,timeout=2):
		#make socket non blocking
		the_socket.setblocking(0)
		
		#total data partwise in an array
		total_data=[];
		data='';
		
		#beginning time
		begin=time.time()
		while 1:
			#if you got some data, then break after timeout
			if total_data and time.time()-begin > timeout:
				break
			
			#if you got no data at all, wait a little longer, twice the timeout
			elif time.time()-begin > timeout*2:
				break
			
			#recv something
			try:
				data = the_socket.recv(8192)
				if data:
					total_data.append(data)
					#change the beginning time for measurement
					begin=time.time()
				else:
					#sleep for sometime to indicate a gap
					time.sleep(0.1)
			except:
				pass
		
		#join all parts to make final string
		return ''.join(total_data)



if __name__ == "__main__":

	logFile = LogFile(SERVER_LOG_PATH)

	voteExtractor = VoteExtractor(REGEX_SAY_COMMAND)

	server = Server(SERVER_IP, SERVER_PORT, SERVER_RCON_PWD)

	#server.sendShuffle()

	print(server.requestStatus())

	while False:
		time.sleep(1)

		if logFile.isChanged():

			votation = Votation()

			text = logFile.read()

			for textLine in text:
				vote = voteExtractor.extract(textLine)
				if vote:
					votation.addVote(vote)
			
			votation.calculate()

			Console.info(votation)


