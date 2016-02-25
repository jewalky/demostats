# -*- coding: utf-8 -*-

from demo import *
import data
from data import *
from versions.enums212 import *


VERBOSE = False



lastlocaluserinfo = None

class TeamState:
    def __init__(self):
        self.flagdropped = False
        self.flagtaken = False
        self.flagheldby = None
        self.flagwasdropped = False
        

# as of now, only two teams are supported
teamstates = {'Blue': TeamState(), 'Red': TeamState()}
teamnames = ['Blue', 'Red']


def MAKE_ID(d, c, b, a):
    return (ord(a) << 24) | (ord(b) << 16) | (ord(c) << 8) | (ord(d))


def GetPlayerByName(name):
    name = V_CleanPlayerName(name)
    for player in data.players:
        if player.userinfo.netname is not None and\
           V_CleanPlayerName(player.userinfo.netname) == name:
            return player
    return None
    
    
def DEMOSTATS_FlagTaken(teamname, player):
    if VERBOSE:
        print('%s flag taken! (by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    # check if flag was dropped. if it was dropped, don't award touch.
    if not teamstates[teamname].flagwasdropped:
        player.stats_touches += 1
    
    
def DEMOSTATS_FlagReturned(teamname, player):
    if VERBOSE:
        print('%s flag returned. (by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    player.stats_returns += 1
    
    
def DEMOSTATS_Capture(teamname, player):
    if VERBOSE:
        print('%s team scores! (by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    # captures aren't counted towards touches
    if not teamstates[teamname].flagwasdropped:
        player.stats_touches -= 1
        player.stats_captures += 1
    else:
        player.stats_pickups += 1
    
    
def DEMOSTATS_Assist(teamname, player):
    if VERBOSE:
        print('%s team scores! (assisted by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    player.stats_assists += 1
    
    
def DEMOSTATS_FlagDropped(teamname):
    if VERBOSE:
        print('%s flag dropped. (last held by: %s)' % (teamname, V_CleanPlayerName(teamstates[teamname].flagheldby.userinfo.netname)))
    
    
def DEMOSTATS_PlayerDied(deadplayer, player):
    # deadplayer is the one who died.
    # player is the one who killed.
    #print('%s pkilled %s.' % (V_CleanPlayerName(player.userinfo.netname), V_CleanPlayerName(deadplayer.userinfo.netname)))
    # too much flood
    if deadplayer == player or player is None: # suicide or slime
        return
    player.stats_frags += 1
    # check defend.
    # defend is when deadplayer was holding a flag, and player killed him.
    global teamstates
    for teamname in teamstates:
        if teamstates[teamname].flagheldby == deadplayer and player.lastteam == teamname:
            player.stats_defends += 1
    
    
def DEMOSTATS_MapEnded():
    splayers = []
    for player in data.players:
        if player.ingame and not player.spectating:
            splayers.append(player)
    if len(splayers) <= 0:
        return

    splayers = sorted(splayers, key=lambda splayer: splayer.stats_captures+splayer.stats_pickups, reverse=True)
    splayers = sorted(splayers, key=lambda splayer: splayer.lastteam)
    
    print('=========================================================================')
    print(' Player                          TEAM  CPT  FRG  PKP  TCH  AST  DEF  RET')
    print('-------------------------------------------------------------------------')
    
    for player in splayers:
        print('%-32s %-5s %-4d %-4d %-4d %-4d %-4d %-4d %-4d' %
            (V_CleanPlayerName(player.userinfo.netname),
             player.lastteam.upper(),
             player.stats_captures, player.stats_frags, player.stats_pickups, player.stats_touches,
             player.stats_assists, player.stats_defends, player.stats_returns))

    print('-------------------------------------------------------------------------')
    
    
def DEMOSTATS_InitPlayer(player, forced=False):
    #Captures, frags, pickups, touches, assists, defences, returns.
    if hasattr(player, 'stats_captures') and not forced:
        return
    player.stats_captures = 0
    player.stats_frags = 0
    player.stats_pickups = 0
    player.stats_touches = 0
    player.stats_assists = 0
    player.stats_defends = 0
    player.stats_returns = 0
    
    
lastteamname = None
lastplayername = None
lasttic = None
leveltic = 0
def DEMOSTATS_Callback(packet):
    global consoleplayer
    global players
    global lastlocaluserinfo
    global teamstates
    global teamnames
    global lastteamname
    global lastplayername
    global lasttic
    global leveltic
    
    if packet.name != 'CLD_TICCMD' and packet.name != 'SVC_MOVEPLAYER' and packet.name != 'SVC_MOVELOCALPLAYER':
        #print(repr(packet))
        pass
        
    if packet.name == 'CLD_TICCMD':
        leveltic += 1
        
    elif packet.name == 'SVC_MAPLOAD':
        # display stats from last map
        DEMOSTATS_MapEnded()
        
        # clear players
        CLIENT_ClearAllPlayers()
        
        # restore local userinfo
        if lastlocaluserinfo is not None:
            DEMOSTATS_Callback(lastlocaluserinfo)
        
        # print
        print('Current map is %s (changemap)' % (packet.map))

    elif packet.name == 'SVC_SETGAMEMODE':
        if packet.gamemode != GAMEMODE_CTF: #
            print('Error: CTF gamemode is required.')
            exit(1)
    
    elif packet.name == 'SVCC_AUTHENTICATE':
        # display stats from last map
        DEMOSTATS_MapEnded()
    
        # restore local userinfo
        if lastlocaluserinfo is not None:
            DEMOSTATS_Callback(lastlocaluserinfo)

    elif packet.name == 'SVC_SETPLAYERTEAM':
        if packet.team < len(teamnames):
            players[packet.player].lastteam = teamnames[packet.team]
            players[packet.player].team = teamnames[packet.team]
        else:
            players[packet.player].team = 'None'
            
    elif packet.name == 'SVC_SPAWNPLAYER':
        players[packet.player].spectating = packet.spectating # important!
        players[packet.player].bot = packet.bot
        players[packet.player].ingame = True
        players[packet.player].netid = packet.body_netid # this is used for frags
        
    elif packet.name == 'SVC_KILLPLAYER':
        # killed player
        deadplayer = players[packet.player]
        player = None
        for splayer in players:
            if not hasattr(splayer, 'netid'):
                continue
            if splayer.netid == packet.source_netid:
                player = splayer
                break
        if player is not None:
            DEMOSTATS_PlayerDied(deadplayer, player)
        
    elif packet.name == 'SVC_PLAYERISSPECTATOR':
        players[packet.player].spectating = True
            
    elif packet.name == 'SVC_DISCONNECTPLAYER':
        players[packet.player] = Player()
        
    elif packet.name == 'SVC_SETCONSOLEPLAYER':
        oldconsoleplayer = data.consoleplayer
        data.consoleplayer = packet.player
        players[data.consoleplayer] = players[oldconsoleplayer]
        players[oldconsoleplayer] = Player()
        
    elif packet.name == 'CLD_USERINFO' or packet.name == 'SVC_SETPLAYERUSERINFO':
        # update userinfo. currently only care about the name
        if hasattr(packet, 'player'):
            userinfo = players[packet.player].userinfo
            DEMOSTATS_InitPlayer(players[packet.player])
        else:
            userinfo = players[data.consoleplayer].userinfo
            DEMOSTATS_InitPlayer(players[data.consoleplayer])
            lastlocaluserinfo = packet

        oldname = userinfo.netname
        userinfo.netname = packet.userinfo['name']
        if oldname is not None and userinfo.netname.lower() != oldname.lower():
            print('%s is now known as %s' % (V_CleanPlayerName(oldname), V_CleanPlayerName(userinfo.netname)))
            
    elif packet.name == 'SVC_TEAMFLAGRETURNED':
        if lastplayername is not None and lasttic == leveltic:
            teamname = teamnames[packet.team]
            DEMOSTATS_FlagReturned(teamname, GetPlayerByName(lastplayername))
            teamstates[teamname].flagtaken = False
            teamstates[teamname].flagdropped = False
            teamstates[teamname].flagwasdropped = False
            teamstates[teamname].flagheldby = None
            lastplayername = None
            
    elif packet.name == 'SVC_TEAMFLAGDROPPED':
        teamname = teamnames[packet.team]
        DEMOSTATS_FlagDropped(teamname)
        teamstates[teamname].flagtaken = False
        teamstates[teamname].flagdropped = True
        teamstates[teamname].flagwasdropped = True
        teamstates[teamname].flagheldby = None
            
    elif packet.name == 'SVC_PRINTHUDMESSAGEFADEOUT':
        # YOU HAVE THE ... FLAG
        #if packet.string.find('scores') >= 0:
        #    print(repr(packet))
        if packet.msgid == MAKE_ID('C','N','T','R'):
            s = V_CleanPlayerName(V_ColorizeString(packet.string))
            if s.find('You have the ') == 0 and s[-6:] == ' flag!':
                teamname = s[13:-6]
                DEMOSTATS_FlagTaken(teamname, data.players[data.consoleplayer])
                teamstates[teamname].flagtaken = True
                teamstates[teamname].flagdropped = False
                teamstates[teamname].flagheldby = data.players[data.consoleplayer]
                lastteamname = None
            elif s[-12:] == ' flag taken!':
                teamname = s[:-12]
                lastteamname = teamname
                lasttic = leveltic
            elif s[-13:] == ' team scores!':
                teamname = s[:-13]
                lastteamname = teamname
                lasttic = leveltic
        if packet.msgid == MAKE_ID('S','U','B','S'):
            s = V_CleanPlayerName(V_ColorizeString(packet.string))
            if s.find('Held by: ') == 0:
                playername = s[9:]
                if lastteamname is not None and lasttic == leveltic:
                    pl = GetPlayerByName(playername)
                    DEMOSTATS_FlagTaken(lastteamname, pl)
                    teamstates[lastteamname].flagtaken = True
                    teamstates[lastteamname].flagdropped = False
                    teamstates[lastteamname].flagheldby = pl
                    lastteamname = None
            elif s.find('Returned by: ') == 0:
                playername = s[13:]
                lastplayername = playername
                lasttic = leveltic
            elif s.find('Scored by: ') == 0:
                if lastteamname is not None and lasttic == leveltic:
                    lines = s.split('\n')
                    playername = lines[0][11:]
                    if len(lines) > 1 and lines[1].find('Assisted by: ') == 0:
                        playernameassist = lines[1][13:]
                    else:
                        playernameassist = None
                    DEMOSTATS_Capture(lastteamname, GetPlayerByName(playername))
                    if playernameassist is not None:
                        DEMOSTATS_Assist(lastteamname, GetPlayerByName(playernameassist))
                    # check whatever team had the capturing player and release it's flag
                    for teamname in teamstates:
                        if teamstates[teamname].flagheldby is not None and\
                           teamstates[teamname].flagheldby.userinfo.netname == playername:
                            teamstates[teamname].flagtaken = False
                            teamstates[teamname].flagdropped = False
                            teamstates[teamname].flagwasdropped = False
                            teamstates[teamname].flagheldby = None
                    lastteamname = None
    

if __name__ != '__main__':
    raise ImportError('Can\'t import entrypoint file')
    
if len(sys.argv) < 2:
    print('Usage: %s <demo file name>' % (sys.argv[0]))
    exit(1)
CLIENTDEMO_Read(sys.argv[1], DEMOSTATS_Callback)
