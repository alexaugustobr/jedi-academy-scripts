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

REGEX_SAY_COMMAND = r'(.[0-9]*:.[0-9]*) (.*[0-9]:) (say:) (.*:) ("!(shuffle|sf)")'

REGEX_PLAYER_Disconnected = r'(ClientDisconnect:(.[0-9]*))'

SERVER_RCON_PWD = 'rcon'
SERVER_IP = '127.0.1.1'
SERVER_PORT = 29070

MSG_ONLINE = 'Shuffle votation is on!'

MSG_VOTATION_PASS = 'Shuffle passed!'

MSG_VOTATION_FAIL = 'Shuffle failed!'

MSG_VOTATION_INITIALIZED = 'Shuffle votation initialized!'

VOTATION_MAX_TIME_TO_FAIL = 5

MSG_TOTAL_PLAYERS_WANTS = '{}/{} players wants to shuffle the team!'

MSG_PLAYER_WANT = '{} wants to Shuffle the team!'

MSG_PLAYER_REMOVED_FROM_VOTES = 'Player {} was disconnected his \'shuffle\' vote was been removed.'

DEFAULT_MESSAGE_DECODER = 'iso-8859-1'

LOOP_TIME = 1

LAMBDA_DIGITS = lambda x: int(filter(str.isdigit, x) or None)

IS_DEBUG_ENABLED = True

class Console:
	@staticmethod
	def info(message):
		finalMessage = '({}) INFO: {}'.format(datetime.datetime.now(), message)
		print(finalMessage)
	@staticmethod
	def debug(message):
		if IS_DEBUG_ENABLED:
			finalMessage = '({}) DEBUG: {}'.format(datetime.datetime.now(), message)
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

class PlayerDisconnectedExtractor:

	def __init__(self, regex):
		self.regex = regex

	def extract(self, stringToExtract):
		result = re.search(self.regex, stringToExtract)

		if (not result):
			return None

		playerId = result.group(2).strip()

		return int(LAMBDA_DIGITS(playerId))

class Votation:

	def __init__(self):
		pass

	voteDict = {}
	totalVotes = 0
	totalPlayers = 0

	MIN_PLAYERS_TO_VOTE = 3

	MIN_PERCENT_PLAYERS_TO_WIN = 0.6
	
	def addVote(self, vote):
		playerId = int(LAMBDA_DIGITS(vote.playerId))
		self.voteDict[playerId] = vote

	def playerHasVoted(self, playerId):
		return playerId in self.voteDict.keys()

	def removeVote(self, playerId):
		if playerId in self.voteDict.keys():
			del self.voteDict[playerId]

	def calculate(self):
		self.totalVotes = len(self.voteDict.keys())

	def reset(self):
		self.voteDict = {}
		self.totalVotes = 0
		self.totalPlayers = 0

	def isPassed(self):
		return self.totalVotes >= self.totalVotesNeedToWin()

	def totalVotesNeedToWin(self):
		if self.totalPlayers <= self.MIN_PLAYERS_TO_VOTE:
			return self.MIN_PLAYERS_TO_VOTE
		
		return int(round(self.MIN_PERCENT_PLAYERS_TO_WIN * self.totalPlayers))

	def __str__(self):
		strx = """
		totalVotes = {}
		totalPlayers = {}
		totalVotesNeedToWin = {}
		isPassed = {}
		""".format(self.totalVotes, self.totalPlayers, self.totalVotesNeedToWin(), self.isPassed())
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

	REGEX_PLAYER_COUNT = r'(\\clients\\(.[0-9]*)\\)'

	def __init__(self, host, port, rconPassword):
		self.rconPassword = rconPassword
		self.host = host
		self.port = port

	def sendData(self, data):
		data = ("\xff\xff\xff\xff%s\n" % data)
		#Console.debug("%r"%data)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(data, (self.host, self.port))
		receivedData = self.recvWithTimeout(sock)
		decodeMessage = receivedData.decode(DEFAULT_MESSAGE_DECODER).strip()
		return decodeMessage

	def sendRconCmdWithParameter(self, cmd, parameter):
		data = ("rcon %s %s %s" % (self.rconPassword, cmd, parameter))
		self.sendData(data)

	def sendRconCmd(self, cmd):
		data = ("rcon %s %s" % (self.rconPassword, cmd))
		self.sendData(data)

	def sendCmd(self, cmd):
		return self.sendData(cmd)

	def sendMessage(self, msg):
		Console.info(msg)
		self.sendRconCmdWithParameter("svsay", msg)

	def sendShuffle(self):
		self.sendRconCmd("shuffle")

	def requestStatus(self):
		return self.sendCmd("getstatus")

	def requestInfo(self):
		return self.sendCmd("getinfo")

	def requestPlayerCount(self):
		info = self.requestInfo()

		#igore all escape characters, because the string come just like this \clients\
		raw_txt = "%r"%info

		result = re.search(self.REGEX_PLAYER_COUNT, raw_txt)

		if not result:
			return 0

		textNumber = result.group(2)	

		return LAMBDA_DIGITS(textNumber)

	def recvWithTimeout(self, the_socket,timeout=2):
		#make socket non blocking
		the_socket.setblocking(0)
		#total data partwise in an array
		total_data=[];
		data='';
		#beginning time
		begin=time.time()
		while True:
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

	playerDisconnectedExtractor = PlayerDisconnectedExtractor(REGEX_PLAYER_Disconnected)

	server = Server(SERVER_IP, SERVER_PORT, SERVER_RCON_PWD)

	while True:
		time.sleep(LOOP_TIME)

		votation = Votation()

		if logFile.isChanged():

			votation.totalPlayers = server.requestPlayerCount()

			text = logFile.read()

			for textLine in text:

				vote = voteExtractor.extract(textLine)

				if vote:
					votation.addVote(vote)
					server.sendMessage(MSG_PLAYER_WANT.format(vote.playerName))
				
				disconnectedPlayerId = playerDisconnectedExtractor.extract(textLine)

				if disconnectedPlayerId and votation.playerHasVoted(disconnectedPlayerId):
					votation.removeVote(disconnectedPlayerId)
					server.sendMessage(MSG_PLAYER_REMOVED_FROM_VOTES.format(disconnectedPlayerId))
				
				if votation.totalVotes > 0:
					server.sendMessage(MSG_TOTAL_PLAYERS_WANTS.format(votation.totalVotes, votation.totalPlayers))
			
			votation.calculate()

			Console.info(votation)

			if votation.isPassed():
				server.sendShuffle()
				server.sendMessage(MSG_TOTAL_PLAYERS_WANTS.format(votation.totalVotes, votation.totalPlayers))
				server.sendMessage(MSG_VOTATION_PASS)
				votation.reset()
			else:
				if votation.totalVotes > 0:
					server.sendMessage(MSG_TOTAL_PLAYERS_WANTS.format(votation.totalVotes, votation.totalPlayers))
			
	

			


