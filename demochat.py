# -*- coding: utf-8 -*-

from demo import *
import data
from data import *


lastlocaluserinfo = None


def DEMOSTATS_Callback(packet):
    global consoleplayer
    global players
    global lastlocaluserinfo

    if packet.name == 'SVCC_AUTHENTICATE':
        # restore local userinfo
        if lastlocaluserinfo is not None:
            DEMOSTATS_Callback(lastlocaluserinfo)
            
    elif packet.name == 'SVC_SPAWNPLAYER':
        players[packet.player].spectating = packet.spectating # important!
        players[packet.player].bot = packet.bot
        
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
        else:
            userinfo = players[data.consoleplayer].userinfo
            lastlocaluserinfo = packet

        oldname = userinfo.netname
        userinfo.netname = packet.userinfo['name']
        if oldname is not None and userinfo.netname.lower() != oldname.lower():
            print('%s is now known as %s' % (V_CleanPlayerName(oldname), V_CleanPlayerName(userinfo.netname)))
            
    elif packet.name == 'SVC_PLAYERSAY':
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
