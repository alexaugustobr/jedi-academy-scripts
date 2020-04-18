
"""
(.[0-9]*:.[0-9]*) (.*[0-9]:) (say:) (.*:) ("![s|n|y|N|S|Y|0|1]")
	*  30:04 0: say: ^2Tigao: "lol"
	*  0:22 say: Server: lol say:
	* * 35:52 ClientDisconnect: 0
	* (?:intended)(.*)(?:to match)
"""

import re
import datetime
import time
import os
import socket

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

class LogFile():
	def __init__(self, serverLogPath):
		self.serverLogPath = serverLogPath
		self._cached_stamp = 0
		self._lastLineNumber = 1

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


if __name__ == "__main__":

	logFile = LogFile(SERVER_LOG_PATH)

	while True:
		time.sleep(LOOP_TIME)

		#if logFile.isChanged():





"""
txt = """
u'\xff\xff\xff\xffstatusResponse\n\\fraglimit\\15\\timelimit\\0\\g_gametype\\7\\sv_hostname\\^0[^1SS^77^0] ^1 ^1The Farm [Cheats On]\\sv_maxclients\\32\\sv_maxRate\\25000\\sv_minPing\\0\\sv_maxPing\\0\\sv_floodProtect\\1\\g_ShuffleTimer\\300\\g_autoteambalance\\0\\g_allowunbalance\\1\\sv_maxConnections\\3\\g_Authenticity\\0\\g_allowedHeroClasses\\0\\g_allowedVillainClasses\\0\\g_TimePeriod\\0\\g_EUAllowed\\1\\g_AntiCheat\\1\\g_TKPointsSpecCount\\9999400\\g_TKPointsKickCount\\9999900\\g_noSpecMove\\0\\g_HideHUDFromSpecs\\1\\g_maxGameClients\\0\\g_jediVmerc\\1\\version\\JAmp: v1.0.1.1 linux-i386 Nov 10 2003\\dmflags\\0\\capturelimit\\0\\g_maxHolocronCarry\\3\\g_privateDuel\\1\\g_saberLocking\\1\\g_maxForceRank\\6\\duel_fraglimit\\10\\g_forceBasedTeams\\0\\g_duelWeaponDisable\\1\\g_needpass\\0\\protocol\\26\\mapname\\legosw\\sv_allowDownload\\0\\bot_minplayers\\0\\gamename\\Movie Battles II V1.5.3\\g_gravity\\800\\g_SiegeClassQueue\\aaaaaaaaaaaa\\bg_fighterAltControl\\0\n0 999 "s1"\n0 999 "j1"\n0 999 "^0[^1SS^77^0] ^1Daniel the Dron"'
"""

print(txt.split('\n'))


"""
"""

DEFAULT_MESSAGE_DECODER = 'iso-8859-1'

REGEX_PLAYER_COUNT = r'(\\clients\\(.[0-9]*)\\)'

txt = '\game\MBII\fdisable\0\wdisable\31\truejedi\1\needpass\0\gametype\7\sv_maxclients\32\clients\3\mapname\legosw\hostname\^0[^1SS^77^0] ^1 ^1The Farm [Cheats On]\protocol\26'
raw_txt = "%r"%txt

import re

result = re.search(REGEX_PLAYER_COUNT, raw_txt)

num = result.group(2)

digit = lambda x: int(filter(str.isdigit, x) or 0)

print(digit(num))


"""

"""
txt = '\xff\xff\xff\xffprint\nmap: legosw\n\xff\xff\xff\xffprint\nnum score ping name            lastmsg address               qport rate\n\xff\xff\xff\xffprint\n--- ----- ---- --------------- ------- --------------------- ----- -----\n\xff\xff\xff\xffprint\n  0     0   24 s1                   25   192.168.1.101:29071 54630 25000\n\xff\xff\xff\xffprint\n  1     0   24 j1                   25   192.168.1.101:29072 14359 25000\n\xff\xff\xff\xffprint\n  2     0   24 ^0[^1SS^77^0] ^      25   192.168.1.101:29073 33266 25000\n\xff\xff\xff\xffprint\n\n\xff\xff\xff\xffprint\n'


nt = txt.decode(DEFAULT_MESSAGE_DECODER)\
        .strip()\
        .replace('\xff\xff\xff\xffprint\n'.decode(DEFAULT_MESSAGE_DECODER), '')\
        .replace('\xff\xff\xff\xffprint'.decode(DEFAULT_MESSAGE_DECODER), '')

print(nt)

class PlayerInfo:
    def __init__(self, num, score, ping, name, lastmsg, address, qport, rate):
        self.num = num
        self.score = score
        self.ping = ping
        self.name = name
        self.lastmsg = lastmsg
        self.address = address
        self.qport = qport
        self.rate = rate
        
COLMUNS = 'num score ping name            lastmsg address               qport rate'
SEPARTOR = '---'
MAP = 'map: '

textLineList = nt.split('\n')
playerList = []

for i in range(0, len(textLineList)):

    #ignore the first lines
    if i < 3:
        continue

    textLine = textLineList[i]

    if textLine.strip() == "":
        continue
    
    
    num = textLine[0:3].strip()
    score = textLine[4:9].strip()
    ping = textLine[9:14].strip()
    name = textLine[14:30].strip()
    lastmsg = textLine[30:38].strip()
    address = textLine[38:60].strip()
    qport = textLine[60:66].strip()
    rate = textLine[66:72].strip()

    playerInfo = PlayerInfo(num, score, ping, name, lastmsg, address, qport, rate)
    playerList.append(playerInfo)

print(playerList)

num score ping name            lastmsg address               qport rate
0123456789
--- ----- ---- --------------- ------- --------------------- ----- -----
  0     0   24 s1                   25   192.168.1.101:29071 54630 25000
  1     0   24 j1                   25   192.168.1.101:29072 14359 25000
  2     0   24 ^0[^1SS^77^0] ^      25   192.168.1.101:29073 33266 25000
    


"""