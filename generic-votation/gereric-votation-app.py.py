#!/usr/bin/python2

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

SERVER_LOG_PATH = '/home/alex/.ja/MBII/server.log'

#SERVER_ROOT_PWD = ''
#SERVER_IP = ''

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

	REGEX_SAY_COMMAND = r'(.[0-9]*:.[0-9]*) (.*[0-9]:) (say:) (.*:) ("![s|n|y|N|S|Y|0|1]")'

	def extractFromStringWithRegex(self, regex, stringToExtract):
		result = re.search(regex, stringToExtract)
		return result

	def extract(self, stringToExtract):
		result = self.extractFromStringWithRegex(self.REGEX_SAY_COMMAND, stringToExtract)

		if (not result):
			return None

		messageId = result.group(1).strip()
		playerId = result.group(2).strip()
		playerName = result.group(4).strip()
		optionMessage = result.group(5).strip()
		favorable = VoteOptionParser.isFavorable(optionMessage)
		
		return Vote(messageId, playerId, playerName, optionMessage, favorable)

class Scoreboard:

	voteDict = {}
	votesAgainst = 0
	votesInFavor = 0

	def __init__(self):
		pass
	
	def addVote(self, vote):
		self.voteDict[vote.playerId] = vote

	def calculate(self):
		for key in self.voteDict.keys():
			vote = self.voteDict[key]

			if vote.favorable:
				self.votesInFavor = self.votesInFavor + 1
			else:
				self.votesAgainst = self.votesAgainst + 1

	def isPassed(self):
		return self.votesInFavor > self.votesAgainst

	def __str__(self):
		strx = """
		votesAgainst = {}
		votesInFavor = {}
		passed = {}
		""".format(self.votesAgainst, self.votesInFavor, self.isPassed())
		return strx
		

class Vote:

	def __init__(self, messageId, playerId, playerName, optionMessage, favorable):
		self.messageId = messageId
		self.playerId = playerId
		self.playerName = playerName
		self.optionMessage = optionMessage 
		self.favorable = favorable

	def __str__(self):

		strx = """
		messageId = {}
		playerId = {}
		playerName = {}
		optionMessage  = {}
		favorable = {}
		""".format(self.messageId, self.playerId, self.playerName, self.optionMessage, self.favorable)

		return strx

class VoteOptionParser:

	@staticmethod
	def isFavorable(optionMessage):
		REGEX_FAVORABLE_VOTE = r'("![s|y|S|Y|1]")'
		
		result = re.search(REGEX_FAVORABLE_VOTE, optionMessage)
		
		if result:
			return True
		else:
			return False
		
	@staticmethod
	def isAgainst(optionMessage):
		REGEX_AGAINST_VOTE = r'("![n|N|0]")'
		
		result = re.search(REGEX_AGAINST_VOTE, optionMessage)
		
		if result:
			return True
		else:
			return False

if __name__ == "__main__":

	logFile = LogFile(SERVER_LOG_PATH)

	voteExtractor = VoteExtractor()

	while True:
		time.sleep(1)

		if logFile.isChanged():

			scoreboard = Scoreboard()

			text = logFile.read()

			for textLine in text:
				vote = voteExtractor.extract(textLine)
				if vote:
					scoreboard.addVote(vote)
			
			scoreboard.calculate()

			Console.info(scoreboard)


