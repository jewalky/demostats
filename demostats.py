# -*- coding: utf-8 -*-

from demo import *
import data
from data import *
from versions.enums212 import *


VERBOSE = False
VERBOSEFLAG = False


# map stuff
levelname = None
levelreturns = 0


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
    if VERBOSE or VERBOSEFLAG:
        print('%s flag %s! (by: %s)' % (teamname, 'taken' if not teamstates[teamname].flagwasdropped else 'picked up', V_CleanPlayerName(player.userinfo.netname)))
    # check if flag was dropped. if it was dropped, don't award touch.
    if not teamstates[teamname].flagwasdropped:
        player.stats_touches += 1
    else:
        player.stats_pickups += 1
    
    
def DEMOSTATS_FlagReturned(teamname, player):
    global levelreturns
    if player is None:
        if VERBOSE or VERBOSEFLAG:
            print('%s flag returned. (automatically)'%teamname)
        levelreturns += 1
        return
    if VERBOSE or VERBOSEFLAG:
        print('%s flag returned. (by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    player.stats_returns += 1
    
    
def DEMOSTATS_Capture(teamname, player):
    if VERBOSE or VERBOSEFLAG:
        print('%s team scores! (by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    # captures aren't counted towards touches
    # find team which got this player as carrier
    team2 = None
    for teamname2 in teamstates:
        if teamstates[teamname2].flagheldby == player:
            team2 = teamstates[teamname2]
            break
    if team2.flagwasdropped:
        player.stats_pcaptures += 1
    else:
        player.stats_captures += 1
    
    
def DEMOSTATS_Assist(teamname, player):
    if VERBOSE:
        print('%s team scores! (assisted by: %s)' % (teamname, V_CleanPlayerName(player.userinfo.netname)))
    player.stats_assists += 1
    
    
def DEMOSTATS_FlagDropped(teamname):
    if VERBOSE or VERBOSEFLAG:
        print('%s flag dropped. (last held by: %s)' % (teamname, V_CleanPlayerName(teamstates[teamname].flagheldby.userinfo.netname)))
    
    
def DEMOSTATS_PlayerDied(deadplayer, player):
    # deadplayer is the one who died.
    # player is the one who killed.
    if VERBOSE:
        if player is not None:
            print('%s pkilled %s.' % (V_CleanPlayerName(player.userinfo.netname), V_CleanPlayerName(deadplayer.userinfo.netname)))
        else:
            print('%s died.' % (V_CleanPlayerName(deadplayer.userinfo.netname)))
    if player is not None:
        player.stats_frags += 1
    deadplayer.stats_deaths += 1
    # check defend.
    # defend is when deadplayer was holding a flag, and player killed him.
    global teamstates
    for teamname in teamstates:
        if teamstates[teamname].flagheldby == deadplayer and player.lastteam == teamname:
            player.stats_defends += 1
            if not VERBOSE and VERBOSEFLAG:
                print('%s pkilled %s.' % (V_CleanPlayerName(player.userinfo.netname), V_CleanPlayerName(deadplayer.userinfo.netname)))
            DEMOSTATS_FlagDropped(teamname)
            teamstates[teamname].flagheldby = None
            teamstates[teamname].flagwasdropped = True
            teamstates[teamname].flagdropped = True
            teamstates[teamname].flagtaken = False
            
            
def DEMOSTATS_PlayerSpectated(player):
    if VERBOSE:
        print('%s has joined the spectators')
    # drop the flag
    global teamstates
    for teamname in teamstates:
        if teamstates[teamname].flagheldby == player:
            DEMOSTATS_FlagDropped(teamname)
            teamstates[teamname].flagheldby = None
            teamstates[teamname].flagwasdropped = True
            teamstates[teamname].flagdropped = True
            teamstates[teamname].flagtaken = False
            

def DEMOSTATS_PlayerDisconnected(player):
    if VERBOSE:
        print('%s disconnected')
    # drop the flag
    global teamstates
    for teamname in teamstates:
        if teamstates[teamname].flagheldby == player:
            DEMOSTATS_FlagDropped(teamname)
            teamstates[teamname].flagheldby = None
            teamstates[teamname].flagwasdropped = True
            teamstates[teamname].flagdropped = True
            teamstates[teamname].flagtaken = False
    
    
def DEMOSTATS_PlayerJoined(teamname, player):
    if VERBOSE:
        print('%s has joined the %s team.'%(V_CleanPlayerName(player.userinfo.netname), teamname))
    
    
def DEMOSTATS_MapEnded():
    global levelreturns
    global leveltic
    splayers = []
    for player in data.players:
        if player.ingame and not player.wasspectating:
            splayers.append(player)

    if len(splayers) > 0:
        splayers = sorted(splayers, key=lambda splayer: splayer.stats_captures+splayer.stats_pcaptures, reverse=True)
        splayers = sorted(splayers, key=lambda splayer: splayer.lastteam)
        
        print('===============================================================================')
        print(' Player                             TEAM  CAP TCH PCAP PKP FRG DTH AST DEF RET')
        print('-------------------------------------------------------------------------------')
        
        for player in splayers:
            consolestar = ' '
            if player == players[data.consoleplayer]:
                consolestar = '*'
            print('%s%-34s %-5s %-3d %-3d %-4d %-3d %-3d %-3d %-3d %-3d %-3d' %
                (consolestar,
                 V_CleanPlayerName(player.userinfo.netname)[:26],
                 player.lastteam.upper(),
                 player.stats_captures+player.stats_pcaptures, player.stats_touches,
                 player.stats_pcaptures, player.stats_pickups,
                 player.stats_frags, player.stats_deaths,
                 player.stats_assists, player.stats_defends, player.stats_returns))

        print('-------------------------------------------------------------------------------')
        print(' MAP: %s' % levelname.upper())
        leveltime = float(leveltic) / 35
        print(' Time: %d:%02d' % (int(leveltime / 60), int(leveltime % 60)))
        print(' Automatic returns: %d' % levelreturns)
        print('-------------------------------------------------------------------------------')
        
    # clear team states
    teamstates['Red'] = TeamState()
    teamstates['Blue'] = TeamState()
    
    # clear player states
    for player in data.players:
        DEMOSTATS_InitPlayer(player, forced=True)
    levelreturns = 0
    leveltic = 0
    
    
def DEMOSTATS_InitPlayer(player, forced=False):
    #Captures, frags, pickups, touches, assists, defences, returns.
    if hasattr(player, 'stats_captures') and not forced:
        return
    player.stats_captures = 0
    player.stats_pcaptures = 0
    player.stats_frags = 0
    player.stats_deaths = 0
    player.stats_pickups = 0
    player.stats_touches = 0
    player.stats_assists = 0
    player.stats_defends = 0
    player.stats_returns = 0
    player.wasspectating = True
    
    
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
    global levelname
    
    if packet.name != 'CLD_TICCMD' and packet.name != 'SVC_MOVEPLAYER' and packet.name != 'SVC_MOVELOCALPLAYER':
        #print(repr(packet))
        pass
        
    if packet.name == 'CLD_TICCMD':
        leveltic += 1
        
    elif packet.name == 'SVC_SETMAPTIME':
        if packet.tics > leveltic:
            leveltic = packet.tics
        
    elif packet.name == 'SVC_MAPLOAD':
        # display stats from last map
        DEMOSTATS_MapEnded()
        
        # print
        levelname = packet.map
        print('Current map is %s (changemap)' % (packet.map.upper()))
        
    elif packet.name == 'CLD_DEMOEND':
        DEMOSTATS_MapEnded()

    elif packet.name == 'SVC_SETGAMEMODE':
        if packet.gamemode != GAMEMODE_CTF: #
            print('Error: CTF gamemode is required.')
            exit(1)
    
    elif packet.name == 'SVCC_AUTHENTICATE':
        # display stats from last map
        DEMOSTATS_MapEnded()
        
        levelname = packet.map
        # restore local userinfo
        if lastlocaluserinfo is not None:
            DEMOSTATS_Callback(lastlocaluserinfo)

    elif packet.name == 'SVC_SETPLAYERTEAM':
        if packet.team < len(teamnames):
            players[packet.player].lastteam = teamnames[packet.team]
            players[packet.player].team = teamnames[packet.team]
            DEMOSTATS_PlayerJoined(teamnames[packet.team], players[packet.player])
        else:
            players[packet.player].team = 'None'
            
    elif packet.name == 'SVC_SPAWNPLAYER':
        cspec = not hasattr(players[packet.player], 'spectating') or players[packet.player].spectating
        if cspec != packet.spectating:
            DEMOSTATS_PlayerSpectated(players[packet.player])
        players[packet.player].spectating = packet.spectating # important!
        if not players[packet.player].spectating:
            players[packet.player].wasspectating = False
        if not hasattr(players[packet.player], 'wasspectating'):
            players[packet.player].wasspectating = True
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
        cspec = not hasattr(players[packet.player], 'spectating') or players[packet.player].spectating
        if cspec != True:
            DEMOSTATS_PlayerSpectated(players[packet.player])
        players[packet.player].spectating = True
            
    elif packet.name == 'SVC_DISCONNECTPLAYER':
        DEMOSTATS_PlayerDisconnected(players[packet.player])
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
        teamname = teamnames[packet.team]
        if lastplayername is not None and lasttic == leveltic:
            DEMOSTATS_FlagReturned(teamname, GetPlayerByName(lastplayername))
            lastplayername = None
        else:
            DEMOSTATS_FlagReturned(teamname, None)
        teamstates[teamname].flagtaken = False
        teamstates[teamname].flagdropped = False
        teamstates[teamname].flagwasdropped = False
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
                    elif len(lines) > 1 and lines[1] == '[ Self-Assisted ]':
                        playernameassist = playername
                    else:
                        playernameassist = None
                    pl = GetPlayerByName(playername)
                    DEMOSTATS_Capture(lastteamname, pl)
                    if playernameassist is not None:
                        DEMOSTATS_Assist(lastteamname, GetPlayerByName(playernameassist))
                    # check whatever team had the capturing player and release it's flag
                    for teamname in teamstates:
                        if teamstates[teamname].flagheldby is not None and\
                           teamstates[teamname].flagheldby == pl:
                            teamstates[teamname].flagtaken = False
                            teamstates[teamname].flagdropped = False
                            teamstates[teamname].flagwasdropped = False
                            teamstates[teamname].flagheldby = None
                    lastteamname = None
                    
    elif packet.name == 'SVC_PLAYERSAY':
        if VERBOSE:
            player = players[packet.player]
            mode = ''
            if packet.mode == 2: # team
                if player.spectating:
                    mode = '<SPEC> '
                else:
                    mode = '<TEAM> '
            if packet.string[:3] != '/me':
                print('%s%s: %s'%(mode, V_CleanPlayerName(player.userinfo.netname), V_CleanPlayerName(V_ColorizeString(packet.string))))
            else:
                print('%s * %s%s'%(mode, V_CleanPlayerName(player.userinfo.netname), V_CleanPlayerName(V_ColorizeString(packet.string[3:]))))

    

if __name__ != '__main__':
    raise ImportError('Can\'t import entrypoint file')
    
if len(sys.argv) < 2:
    print('Usage: %s <demo file name>' % (sys.argv[0]))
    exit(1)
CLIENTDEMO_Read(sys.argv[1], DEMOSTATS_Callback)
