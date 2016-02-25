# -*- coding: utf-8 -*-

from stream import *
from data import *
import enums
import enums212
from enums212 import *
from demo import *

# for strftime
import time
from datetime import datetime


def version():
    return ['2.1.2']
    
def next_header(stream):
    lCommand = NETWORK_ReadUByte(stream)
    
    pkt = {'name': enums.to_string(enums212, lCommand, ['CLD_', 'SVC_', 'SVCC_']),
           'id': lCommand}
    
    if lCommand == CLD_USERINFO:
        pkt['userinfo'] = CLIENTDEMO_ReadUserInfo(stream)
        return pkt
        
    elif lCommand == CLD_DEMOWADS:
        ulWADCount = NETWORK_ReadUShort(stream)
        WadNames = []
        for i in range(ulWADCount):
            WadNames.append(NETWORK_ReadString(stream))
        
        demoHash = NETWORK_ReadString(stream)
        demoMapHash = NETWORK_ReadString(stream)
        
        print('Demo is using following resources:')
        for wad in WadNames:
            print(' %s' % wad)
        print('Protected lump checksum: %s'%demoHash)
        print('Map checksum: %s'%demoMapHash)
        return pkt

    return None

    
def next_packet(stream):
    lCommand = NETWORK_ReadUByte(stream)
    
    pkt = {'name': enums.to_string(enums212, lCommand, ['CLD_', 'SVC_', 'SVCC_']),
           'id': lCommand}
    
    if lCommand == CLD_USERINFO:
        stream.seek(stream.tell()-1)
        return next_header(stream)
    
    elif lCommand == CLD_TICCMD:
        pkt['cmd'] = CLIENTDEMO_ReadTiccmd(stream)
        # also when it's CLD_TICCMD, it's the right time
        # to do end-of-tic stuff in the callback
        return pkt
        
    elif lCommand == CLD_LOCALCOMMAND:
        LCMD = NETWORK_ReadUByte(stream)
        pkt['lcmd_name'] = enums.to_string(enums212, LCMD, ['LCMD_'])
        pkt['lcmd'] = LCMD
        if LCMD == LCMD_INVUSE:
            pkt['item'] = NETWORK_ReadString(stream)
        elif LCMD == LCMD_CENTERVIEW:
            pass
        elif LCMD == LCMD_TAUNT:
            pass
        elif LCMD == LCMD_NOCLIP:
            pass
        return pkt
        
    elif lCommand == CLD_DEMOEND:
        return pkt
        
    # actual client commands go now
    # SVCC stuff
    elif lCommand == SVCC_AUTHENTICATE:
        print('Connected!')
        pkt['map'] = NETWORK_ReadString(stream)
        pkt['gametic'] = NETWORK_ReadULong(stream)
        print('Current map is %s'%pkt['map'])
        CLIENT_ClearAllPlayers()
        return pkt
        
    elif lCommand == SVCC_MAPLOAD:
        pkt['gamemode'] = NETWORK_ReadUByte(stream)
        print('Level authenticated!')
        return pkt
        
    elif lCommand == SVCC_ERROR:
        ulErrorCode = NETWORK_ReadUByte(stream)
        pkt['errorcode_name'] = enums.to_string(enums212, ulErrorCode, ['NETWORK_ERRORCODE_'])
        pkt['errorcode'] = ulErrorCode
        if ulErrorCode == NETWORK_ERRORCODE_WRONGPASSWORD:
            print('Incorrect password.')
        elif ulErrorCode == NETWORK_ERRORCODE_WRONGVERSION:
            pkt['server_version'] = NETWORK_ReadString(stream)
            print('Failed connect. Your version is different.\nThis server is using version: %s'%pkt['server_version'])
        elif ulErrorCode == NETWORK_ERRORCODE_WRONGPROTOCOLVERSION:
            print('Failed connect. Your version uses outdated network code.')
        elif ulErrorCode == NETWORK_ERRORCODE_BANNED:
            errstr = 'Couldn\'t connect. You have been banned from this server!'
            ban_reason = NETWORK_ReadString(stream)
            if ban_reason:
                errstr += '\nReason for ban: '+V_CleanPlayerName(ban_reason)
                pkt['ban_reason'] = ban_reason
            ban_expiration = NETWORK_ReadLong(stream)
            if ban_expiration > 0:
                errstr += '\nYour ban expires on: '+time.strftime("%m/%d/%Y %H:%M", time.localtime(ban_expiration))
                pkt['ban_expiration'] = ban_expiration
            print(errstr)
        elif ulErrorCode == NETWORK_ERRORCODE_SERVERISFULL:
            print('Server is full.')
        elif ulErrorCode == NETWORK_ERRORCODE_AUTHENTICATIONFAILED or\
             ulErrorCode == NETWORK_ERRORCODE_PROTECTED_LUMP_AUTHENTICATIONFAILED:
            numServerPWADs = NETWORK_ReadUByte(stream)
            serverPWADs = []
            for i in range(numServerPWADs):
                serverPWADs.append([NETWORK_ReadString(stream), NETWORK_ReadString(stream)])
            print('%s authentication failed.'%('Level' if ulErrorCode == NETWORK_ERRORCODE_AUTHENTICATIONFAILED else 'Protected lump'))
            print('The server reports %d pwad(s):'%numServerPWADs)
            for pwad in serverPWADs:
                print('PWAD: %s - %s'%pwad)
        elif ulErrorCode == NETWORK_ERRORCODE_FAILEDTOSENDUSERINFO:
            print('Failed to send userinfo.')
        elif ulErrorCode == NETWORK_ERRORCODE_TOOMANYCONNECTIONSFROMIP:
            print('Too many connections from your IP.')
        elif ulErrorCode == NETWORK_ERRORCODE_USERINFOREJECTED:
            print('The server rejected the userinfo.')
        else:
            print('Unknown error code: %d!'%ulErrorCode)
        return pkt
        
    # SVC stuff
    elif lCommand == SVC_HEADER:
        pkt['sequence'] = NETWORK_ReadLong(stream)
        print('Warning: SVC_HEADER in demo stream!')
        return pkt
        
    elif lCommand == SVC_PING:
        pkt['server_time'] = NETWORK_ReadLong(stream)
        return pkt
    
    elif lCommand == SVC_NOTHING:
        return pkt
    
    elif lCommand == SVC_BEGINSNAPSHOT:
        print('Receiving snapshot...')
        return pkt
        
    elif lCommand == SVC_ENDSNAPSHOT:
        print('Snapshot received.')
        return pkt
        
    elif lCommand == SVC_SPAWNPLAYER:
        client_SpawnPlayer(pkt, stream, False)
        return pkt
        
    elif lCommand == SVC_SPAWNMORPHPLAYER:
        client_SpawnPlayer(pkt, stream, True)
        return pkt
        
    elif lCommand == SVC_MOVEPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['flags'] = NETWORK_ReadUByte(stream)
        if (pkt['flags'] & PLAYER_VISIBLE) == PLAYER_VISIBLE:
            pkt['visible'] = True
            pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                               FIXED2FLOAT(NETWORK_ReadLong(stream)),
                               FIXED2FLOAT(NETWORK_ReadShort(stream)<<16)]
            pkt['angle'] = NETWORK_ReadLong(stream)
            pkt['velocity'] = [float(NETWORK_ReadShort(stream)),
                               float(NETWORK_ReadShort(stream)),
                               float(NETWORK_ReadShort(stream))]
            pkt['crouching'] = NETWORK_ReadUByte(stream) != 0
        else:
            pkt['visible'] = False
        return pkt
            
    elif lCommand == SVC_DAMAGEPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['health'] = NETWORK_ReadShort(stream)
        pkt['armor'] = NETWORK_ReadShort(stream)
        pkt['attacker_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_KILLPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['source_netid'] = NETWORK_ReadShort(stream)
        pkt['inflictor_netid'] = NETWORK_ReadShort(stream)
        pkt['health'] = NETWORK_ReadShort(stream)
        pkt['mod'] = NETWORK_ReadString(stream)
        pkt['damagetype'] = NETWORK_ReadString(stream)
        pkt['weapontype'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERHEALTH:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['health'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERARMOR:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['armor'] = NETWORK_ReadShort(stream)
        pkt['armor_icon_name'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERSTATE:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['state'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERUSERINFO:
        pkt['player'] = NETWORK_ReadUByte(stream)
        ulPlayer = pkt['player']
        uin = {}
        flags = NETWORK_ReadShort(stream)
        if (flags & USERINFO_NAME) != 0:
            uin['name'] = NETWORK_ReadString(stream)
        if (flags & USERINFO_GENDER) != 0:
            uin['gender'] = NETWORK_ReadUByte(stream)
        if (flags & USERINFO_COLOR) != 0:
            uin['color'] = NETWORK_ReadULong(stream)
        if (flags & USERINFO_RAILCOLOR) != 0:
            uin['rail_color'] = NETWORK_ReadULong(stream)
        if (flags & USERINFO_SKIN) != 0:
            uin['skin'] = NETWORK_ReadString(stream)
        if (flags & USERINFO_HANDICAP) != 0:
            uin['handicap'] = NETWORK_ReadUByte(stream)
        if (flags & USERINFO_TICSPERUPDATE) != 0:
            uin['ticsperupdate'] = NETWORK_ReadUByte(stream)
        if (flags & USERINFO_CONNECTIONTYPE) != 0:
            uin['connectiontype'] = NETWORK_ReadUByte(stream)
        if (flags & USERINFO_CLIENTFLAGS) != 0:
            uin['clientflags'] = NETWORK_ReadUByte(stream)
        pkt['userinfo'] = uin
        return pkt
        
    elif lCommand == SVC_SETPLAYERFRAGS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['fragcount'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERPOINTS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['pointcount'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERWINS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['wins'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERKILLCOUNT:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['killcount'] = NETWORK_ReadShort(stream)
        return pkt

    elif lCommand == SVC_SETPLAYERCHATSTATUS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['chatting'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETPLAYERCONSOLESTATUS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['inconsole'] = NETWORK_ReadUByte(stream) != 0
        return pkt
    
    elif lCommand == SVC_SETPLAYERLAGGINGSTATUS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['lagging'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETPLAYERREADYTOGOONSTATUS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['readytogoon'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETPLAYERTEAM:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['team'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERCAMERA:
        # always affects console player
        pkt['camera_netid'] = NETWORK_ReadShort(stream)
        pkt['revert'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETPLAYERPOISONCOUNT:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['poisoncount'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERAMMOCAPACITY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['ammotype'] = NETWORK_ReadUShort(stream)
        pkt['maxamount'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERCHEATS:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['cheats'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERPENDINGWEAPON:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['weapontype'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERPSPRITE:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['state'] = NETWORK_ReadString(stream)
        pkt['offset'] = NETWORK_ReadUByte(stream)
        pkt['position'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERBLEND:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['blend'] = [NETWORK_ReadFloat(stream),
                        NETWORK_ReadFloat(stream),
                        NETWORK_ReadFloat(stream),
                        NETWORK_ReadFloat(stream)]
        return pkt
        
    elif lCommand == SVC_SETPLAYERMAXHEALTH:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['maxhealth'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_SETPLAYERLIVESLEFT:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['lives'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_UPDATEPLAYERPING:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['ping'] = NETWORK_ReadShort(stream)
        return pkt
    
    elif lCommand == SVC_UPDATEPLAYEREXTRADATA:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['pitch'] = NETWORK_ReadLong(stream)
        pkt['waterlevel'] = NETWORK_ReadUByte(stream)
        pkt['buttons'] = NETWORK_ReadByte(stream)
        pkt['viewz'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['bob'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_UPDATEPLAYERTIME:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['time'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_MOVELOCALPLAYER:
        pkt['clientticonserverend'] = NETWORK_ReadLong(stream)
        pkt['latestservergametic'] = NETWORK_ReadLong(stream)
        pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream))]
        pkt['velocity'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream))]
        return pkt
        
    elif lCommand == SVC_DISCONNECTPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETCONSOLEPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_CONSOLEPLAYERKICKED:
        return pkt
        
    elif lCommand == SVC_GIVEPLAYERMEDAL:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['medal'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_RESETALLPLAYERSFRAGCOUNT:
        return pkt
        
    elif lCommand == SVC_PLAYERISSPECTATOR:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['dead'] = NETWORK_ReadUByte(stream) != 0
        return pkt
    
    elif lCommand == SVC_PLAYERSAY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['mode'] = NETWORK_ReadUByte(stream)
        pkt['string'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_PLAYERTAUNT:
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_PLAYERRESPAWNINVULNERABILITY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_PLAYERUSEINVENTORY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemtype'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_PLAYERDROPINVENTORY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemtype'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNTHING or lCommand == SVC_SPAWNTHINGNONETID:
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['type'] = NETWORK_ReadUShort(stream)
        if lCommand != SVC_SPAWNTHINGNONETID:
            pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNTHINGEXACT or lCommand == SVC_SPAWNTHINGEXACTNONETID:
        pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream))]
        pkt['type'] = NETWORK_ReadUShort(stream)
        if lCommand != SVC_SPAWNTHINGEXACTNONETID:
            pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_MOVETHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        bits = NETWORK_ReadUShort(stream)
        pkt['position'] = [None, None, None]
        pkt['lastposition'] = [None, None, None]
        pkt['velocity'] = [None, None, None]
        if (bits & CM_X) != 0:
            pkt['position'][0] = float(NETWORK_ReadShort(stream))
        if (bits & CM_Y) != 0:
            pkt['position'][1] = float(NETWORK_ReadShort(stream))
        if (bits & CM_Z) != 0:
            pkt['position'][2] = float(NETWORK_ReadShort(stream))
        if (bits & CM_LAST_X) != 0:
            pkt['lastposition'][0] = float(NETWORK_ReadShort(stream))
        if (bits & CM_LAST_Y) != 0:
            pkt['lastposition'][1] = float(NETWORK_ReadShort(stream))
        if (bits & CM_LAST_Z) != 0:
            pkt['lastposition'][2] = float(NETWORK_ReadShort(stream))
        if (bits & CM_ANGLE) != 0:
            pkt['angle'] = NETWORK_ReadLong(stream)
        if (bits & CM_MOMX) != 0:
            pkt['velocity'][0] = float(NETWORK_ReadShort(stream))
        if (bits & CM_MOMY) != 0:
            pkt['velocity'][1] = float(NETWORK_ReadShort(stream))
        if (bits & CM_MOMZ) != 0:
            pkt['velocity'][2] = float(NETWORK_ReadShort(stream))
        if (bits & CM_PITCH) != 0:
            pkt['pitch'] = NETWORK_ReadLong(stream)
        if (bits & CM_MOVEDIR) != 0:
            pkt['movedir'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_MOVETHINGEXACT:
        pkt['netid'] = NETWORK_ReadShort(stream)
        bits = NETWORK_ReadUShort(stream)
        pkt['position'] = [None, None, None]
        pkt['lastposition'] = [None, None, None]
        pkt['velocity'] = [None, None, None]
        if (bits & CM_X) != 0:
            pkt['position'][0] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_Y) != 0:
            pkt['position'][1] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_Z) != 0:
            pkt['position'][2] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_LAST_X) != 0:
            pkt['lastposition'][0] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_LAST_Y) != 0:
            pkt['lastposition'][1] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_LAST_Z) != 0:
            pkt['lastposition'][2] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_ANGLE) != 0:
            pkt['angle'] = NETWORK_ReadLong(stream)
        if (bits & CM_MOMX) != 0:
            pkt['velocity'][0] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_MOMY) != 0:
            pkt['velocity'][1] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_MOMZ) != 0:
            pkt['velocity'][2] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if (bits & CM_PITCH) != 0:
            pkt['pitch'] = NETWORK_ReadLong(stream)
        if (bits & CM_MOVEDIR) != 0:
            pkt['movedir'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_DAMAGETHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
    
    elif lCommand == SVC_KILLTHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['health'] = NETWORK_ReadShort(stream)
        pkt['damagetype'] = NETWORK_ReadString(stream)
        pkt['source_netid'] = NETWORK_ReadShort(stream)
        pkt['inflictor_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGSTATE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['state'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGTARGET:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['target_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYTHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGANGLE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['angle'] = NETWORK_ReadShort(stream)<<16
        return pkt
        
    elif lCommand == SVC_SETTHINGANGLEEXACT:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['angle'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGWATERLEVEL:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['waterlevel'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGFLAGS:
        pkt['netid'] = NETWORK_ReadShort(stream)
        flagset = NETWORK_ReadUByte(stream)
        flags = NETWORK_ReadULong(stream)
        if flagset == FLAGSET_FLAGS:
            pkt['flags'] = flags
        elif flagset == FLAGSET_FLAGS2:
            pkt['flags2'] = flags
        elif flagset == FLAGSET_FLAGS3:
            pkt['flags3'] = flags
        elif flagset == FLAGSET_FLAGS4:
            pkt['flags4'] = flags
        elif flagset == FLAGSET_FLAGS5:
            pkt['flags5'] = flags
        elif flagset == FLAGSET_FLAGS6:
            pkt['flags6'] = flags
        elif flagset == FLAGSET_FLAGSST:
            pkt['flagsst'] = flags
        return pkt
        
    elif lCommand == SVC_SETTHINGARGUMENTS:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['arguments'] = [NETWORK_ReadByte(stream),
                            NETWORK_ReadByte(stream),
                            NETWORK_ReadByte(stream),
                            NETWORK_ReadByte(stream),
                            NETWORK_ReadByte(stream)]
        return pkt
        
    elif lCommand == SVC_SETTHINGTRANSLATION:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['translation'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGPROPERTY:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['property'] = NETWORK_ReadUByte(stream)
        pkt['value'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGSOUND:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['soundslot'] = NETWORK_ReadUByte(stream)
        pkt['sound'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGSPAWNPOINT:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream))]
        return pkt
        
    elif lCommand == SVC_SETTHINGSPECIAL1 or lCommand == SVC_SETTHINGSPECIAL2:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['special'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGTICS:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['tics'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGTID:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['tid'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_SETTHINGGRAVITY:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['gravity'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETTHINGFRAME or lCommand == SVC_SETTHINGFRAMENF:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['state'] = NETWORK_ReadString(stream)
        pkt['offset'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETWEAPONAMMOGIVE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['ammogive1'] = NETWORK_ReadUShort(stream)
        pkt['ammogive2'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_THINGISCORPSE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['ismonster'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_HIDETHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_TELEPORTTHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['velocity'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['reactiontime'] = NETWORK_ReadShort(stream)
        pkt['angle'] = NETWORK_ReadLong(stream)
        pkt['sourcefog'] = NETWORK_ReadUByte(stream) != 0
        pkt['destinationfog'] = NETWORK_ReadUByte(stream) != 0
        pkt['telezoom'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_THINGACTIVATE or lCommand == SVC_THINGDEACTIVATE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['activator_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_RESPAWNDOOMTHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['fog'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_RESPAWNRAVENTHING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNBLOOD:
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['direction'] = NETWORK_ReadShort(stream) << 16
        pkt['damage'] = NETWORK_ReadUByte(stream)
        pkt['origin_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNBLOODSPLATTER:
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['origin_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNPUFF:
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['pufftype'] = NETWORK_ReadUShort(stream)
        pkt['state'] = NETWORK_ReadUByte(stream)
        translation = NETWORK_ReadUByte(stream) != 0
        if translation:
            pkt['translation'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_PRINT:
        pkt['printlevel'] = NETWORK_ReadUByte(stream)
        pkt['string'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_PRINTMID:
        pkt['string'] = NETWORK_ReadString(stream)
        pkt['bold'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_PRINTMOTD:
        pkt['motd'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_PRINTHUDMESSAGE or\
         lCommand == SVC_PRINTHUDMESSAGEFADEOUT or\
         lCommand == SVC_PRINTHUDMESSAGEFADEINOUT or\
         lCommand == SVC_PRINTHUDMESSAGETYPEONFADEOUT:
        pkt['string'] = NETWORK_ReadString(stream)
        pkt['x'] = NETWORK_ReadFloat(stream)
        pkt['y'] = NETWORK_ReadFloat(stream)
        pkt['width'] = NETWORK_ReadShort(stream)
        pkt['height'] = NETWORK_ReadShort(stream)
        pkt['color'] = NETWORK_ReadUByte(stream)
        if lCommand == SVC_PRINTHUDMESSAGETYPEONFADEOUT:
            pkt['typeontime'] = NETWORK_ReadFloat(stream)
        pkt['holdtime'] = NETWORK_ReadFloat(stream)
        if lCommand == SVC_PRINTHUDMESSAGEFADEINOUT:
            pkt['fadeintime'] = NETWORK_ReadFloat(stream)
        if lCommand != SVC_PRINTHUDMESSAGE:
            pkt['fadeouttime'] = NETWORK_ReadFloat(stream)
        pkt['font'] = NETWORK_ReadString(stream)
        pkt['log'] = NETWORK_ReadUByte(stream) != 0
        pkt['msgid'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETGAMEMODE:
        pkt['gamemode'] = NETWORK_ReadUByte(stream)
        pkt['instagib'] = NETWORK_ReadUByte(stream) != 0
        pkt['buckshot'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETGAMESKILL:
        pkt['gameskill'] = NETWORK_ReadUByte(stream)
        pkt['botskill'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETGAMEDMFLAGS:
        pkt['dmflags'] = NETWORK_ReadULong(stream)
        pkt['dmflags2'] = NETWORK_ReadULong(stream)
        pkt['compatflags'] = NETWORK_ReadULong(stream)
        pkt['zacompatflags'] = NETWORK_ReadULong(stream)
        pkt['zadmflags'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETGAMEMODELIMITS:
        pkt['fraglimit'] = NETWORK_ReadShort(stream)
        pkt['timelimit'] = NETWORK_ReadFloat(stream)
        pkt['pointlimit'] = NETWORK_ReadShort(stream)
        pkt['duellimit'] = NETWORK_ReadByte(stream)
        pkt['winlimit'] = NETWORK_ReadByte(stream)
        pkt['wavelimit'] = NETWORK_ReadByte(stream)
        pkt['sv_cheats'] = NETWORK_ReadUByte(stream) != 0
        pkt['sv_fastweapons'] = NETWORK_ReadByte(stream)
        pkt['sv_maxlives'] = NETWORK_ReadByte(stream)
        pkt['sv_maxteams'] = NETWORK_ReadByte(stream)
        pkt['sv_gravity'] = NETWORK_ReadFloat(stream)
        pkt['sv_aircontrol'] = NETWORK_ReadFloat(stream)
        pkt['sv_coop_damagefactor'] = NETWORK_ReadFloat(stream)
        pkt['alwaysapplydmflags'] = NETWORK_ReadUByte(stream) != 0
        pkt['lobby'] = NETWORK_ReadString(stream)
        pkt['sv_limitcommands'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETGAMEENDLEVELDELAY:
        pkt['delay'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETGAMEMODESTATE:
        pkt['modestate'] = NETWORK_ReadUByte(stream)
        pkt['countdowntics'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_SETDUELNUMDUELS:
        pkt['numduels'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_SETLMSSPECTATORSETTINGS:
        pkt['lmsspectatorsettings'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETLMSALLOWEDWEAPONS:
        pkt['lmsallowedweapons'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETINVASIONNUMMONSTERSLEFT:
        pkt['nummonstersleft'] = NETWORK_ReadShort(stream)
        pkt['numvilesleft'] = NETWORK_ReadShort(stream)
        return pkt

    elif lCommand == SVC_SETINVASIONWAVE:
        pkt['wave'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETSIMPLECTFSTMODE:
        pkt['simple'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_DOPOSSESSIONARTIFACTPICKEDUP:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['ticks'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_DOPOSSESSIONARTIFACTDROPPED:
        return pkt
        
    elif lCommand == SVC_DOGAMEMODEFIGHT:
        pkt['wave'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DOGAMEMODECOUNTDOWN:
        pkt['ticks'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOGAMEMODEWINSEQUENCE:
        pkt['winner'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETDOMINATIONSTATE:
        numpoints = NETWRK_ReadLong(stream)
        pkt['pointowners'] = []
        for i in range(numpoints):
            pkt['pointowners'].append(NETWORK_ReadUByte(stream))
        return pkt
        
    elif lCommand == SVC_SETDOMINATIONPOINTOWNER:
        pkt['point'] = NETWORK_ReadUByte(stream)
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETTEAMFRAGS:
        pkt['team'] = NETWORK_ReadUByte(stream)
        pkt['fragcount'] = NETWORK_ReadShort(stream)
        pkt['announce'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETTEAMSCORE:
        pkt['team'] = NETWORK_ReadUByte(stream)
        pkt['score'] = NETWORK_ReadShort(stream)
        pkt['announce'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETTEAMWINS:
        pkt['team'] = NETWORK_ReadUByte(stream)
        pkt['wins'] = NETWORK_ReadShort(stream)
        pkt['announce'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETTEAMRETURNTICKS:
        pkt['team'] = NETWORK_ReadUByte(stream)
        pkt['ticks'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_TEAMFLAGRETURNED:
        pkt['team'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_TEAMFLAGDROPPED:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['team'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SPAWNMISSILE or lCommand == SVC_SPAWNMISSILEEXACT:
        if lCommand == SVC_SPAWNMISSILE:
            pkt['position'] = [float(NETWORK_ReadShort(stream)),
                               float(NETWORK_ReadShort(stream)),
                               float(NETWORK_ReadShort(stream))]
        else:
            pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                               FIXED2FLOAT(NETWORK_ReadLong(stream)),
                               FIXED2FLOAT(NETWORK_ReadLong(stream))]
        pkt['velocity'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream)),
                           FIXED2FLOAT(NETWORK_ReadLong(stream))]
        pkt['missiletype'] = NETWORK_ReadUShort(stream)
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['target_netid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_MISSILEEXPLODE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['line'] = NETWORK_ReadShort(stream)
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        return pkt
    
    elif lCommand == SVC_WEAPONSOUND:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['sound'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_WEAPONCHANGE:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['weapontype'] = NETWORK_ReadUShort(stream)
        return pkt
        
    elif lCommand == SVC_WEAPONRAILGUN:
        pkt['source_netid'] = NETWORK_ReadShort(stream)
        pkt['start'] = [NETWORK_ReadFloat(stream), NETWORK_ReadFloat(stream), NETWORK_ReadFloat(stream)]
        pkt['end'] = [NETWORK_ReadFloat(stream), NETWORK_ReadFloat(stream), NETWORK_ReadFloat(stream)]
        pkt['color1'] = NETWORK_ReadULong(stream)
        pkt['color2'] = NETWORK_ReadULong(stream)
        pkt['maxdiff'] = NETWORK_ReadFloat(stream)
        pkt['silent'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_SETSECTORFLOORPLANE or lCommand == SVC_SETSECTORCEILINGPLANE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['height'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORFLOORPLANESLOPE or lCommand == SVC_SETSECTORCEILINGPLANESLOPE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['a'] = float(NETWORK_ReadShort(stream))
        pkt['b'] = float(NETWORK_ReadShort(stream))
        pkt['c'] = float(NETWORK_ReadShort(stream))
        return pkt
        
    elif lCommand == SVC_SETSECTORLIGHTLEVEL:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['lightlevel'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORCOLOR or lCommand == SVC_SETSECTORCOLORBYTAG:
        if lCommand == SVC_SETSECTORCOLOR:
            pkt['sector'] = NETWORK_ReadShort(stream)
        else:
            pkt['tag'] = NETWORK_ReadShort(stream)
        r = NETWORK_ReadUByte(stream)
        g = NETWORK_ReadUByte(stream)
        b = NETWORK_ReadUByte(stream)
        pkt['color'] = (r << 16) | (g << 8) | b
        pkt['desaturate'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORFADE or lCommand == SVC_SETSECTORFADEBYTAG:
        if lCommand == SVC_SETSECTORFADE:
            pkt['sector'] = NETWORK_ReadShort(stream)
        else:
            pkt['tag'] = NETWORK_ReadShort(stream)
        r = NETWORK_ReadUByte(stream)
        g = NETWORK_ReadUByte(stream)
        b = NETWORK_ReadUByte(stream)
        pkt['fade'] = (r << 16) | (g << 8) | b
        return pkt
        
    elif lCommand == SVC_SETSECTORFLAT:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['ceiling'] = NETWORK_ReadString(stream)
        pkt['floor'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORPANNING:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['ceiling'] = [NETWORK_ReadShort(stream), NETWORK_ReadShort(stream)]
        pkt['floor'] = [NETWORK_ReadShort(stream), NETWORK_ReadShort(stream)]
        return pkt
        
    elif lCommand == SVC_SETSECTORROTATION or lCommand == SVC_SETSECTORROTATIONBYTAG:
        if lCommand == SVC_SETSECTORROTATION:
            pkt['sector'] = NETWORK_ReadShort(stream)
        else:
            pkt['tag'] = NETWORK_ReadShort(stream)
        # in degrees apparently. Zandronum uses <angle>*ANGLE_1 equation
        pkt['ceiling'] = NETWORK_ReadShort(stream)
        pkt['floor'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORSCALE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['ceiling'] = [NETWORK_ReadShort(stream), NETWORK_ReadShort(stream)]
        pkt['floor'] = [NETWORK_ReadShort(stream), NETWORK_ReadShort(stream)]
        return pkt
        
    elif lCommand == SVC_SETSECTORSPECIAL:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['special'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORFRICTION:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['friction'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['movefactor'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETSECTORANGLEYOFFSET:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['ceilingangle'] = NETWORK_ReadLong(stream)
        pkt['ceilingyoffset'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['floorangle'] = NETWORK_ReadLong(stream)
        pkt['flooryoffset'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETSECTORGRAVITY:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['gravity'] = NETWORK_ReadFloat(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORREFLECTION:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['ceilingreflect'] = NETWORK_ReadFloat(stream)
        pkt['floorreflect'] = NETWORK_ReadFloat(stream)
        return pkt
        
    elif lCommand == SVC_STOPSECTORLIGHTEFFECT:
        pkt['sector'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYALLSECTORMOVERS:
        return pkt
        
    elif lCommand == SVC_DOSECTORLIGHTFIREFLICKER or\
         lCommand == SVC_DOSECTORLIGHTFLICKER or\
         lCommand == SVC_DOSECTORLIGHTLIGHTFLASH:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['maxlight'] = NETWORK_ReadUByte(stream)
        pkt['minlight'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DOSECTORLIGHTSTROBE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['darktime'] = NETWORK_ReadShort(stream)
        pkt['brighttime'] = NETWORK_ReadShort(stream)
        pkt['maxlight'] = NETWORK_ReadUByte(stream)
        pkt['minlight'] = NETWORK_ReadUByte(stream)
        pkt['count'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DOSECTORLIGHTGLOW:
        pkt['sector'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOSECTORLIGHTGLOW2:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['start'] = NETWORK_ReadUByte(stream)
        pkt['end'] = NETWORK_ReadUByte(stream)
        pkt['tics'] = NETWORK_ReadUShort(stream)
        pkt['maxtics'] = NETWORK_ReadUShort(stream)
        pkt['oneshot'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_DOSECTORLIGHTPHASED:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['baselevel'] = NETWORK_ReadUByte(stream)
        pkt['phase'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETLINEALPHA:
        pkt['line'] = NETWORK_ReadShort(stream)
        pkt['alpha'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETLINETEXTURE or lCommand == SVC_SETLINETEXTUREBYID:
        if lCommand == SVC_SETLINETEXTURE:
            pkt['line'] = NETWORK_ReadShort(stream)
        else:
            pkt['tag'] = NETWORK_ReadShort(stream)
        pkt['texture'] = NETWORK_ReadString(stream)
        pkt['side'] = 1 if NETWORK_ReadUByte(stream) != 0 else 0
        pkt['position'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETSOMELINEFLAGS:
        pkt['line'] = NETWORK_ReadShort(stream)
        pkt['flags'] = NETWORK_ReadULong(stream)
        return pkt
        
    elif lCommand == SVC_SETSIDEFLAGS:
        pkt['side'] = NETWORK_ReadShort(stream)
        pkt['flags'] = NETWORK_ReadUByte(stream)
        return pkt
    
    elif lCommand == SVC_ACSSCRIPTEXECUTE:
        pkt['script'] = NETWORK_ReadUShort(stream)
        pkt['activator_netid'] = NETWORK_ReadShort(stream)
        pkt['line'] = NETWORK_ReadShort(stream)
        pkt['levelnum'] = NETWORK_ReadUByte(stream)
        argheader = NETWORK_ReadUByte(stream)
        pkt['args'] = []
        # eh?
        for i in range(3):
            argheader_c = (argheader >> (2 * i)) & 3
            if argheader_c == 1:
                arg = NETWORK_ReadByte(stream)
            elif argheader_c == 2:
                arg = NETWORK_ReadShort(stream)
            elif argheader_c == 3:
                arg = NETWORK_ReadLong(stream)
            else:
                pkt['args'].append(0)
                continue
            pkt['args'].append(arg)
        pkt['backside'] = ((argheader >> 6) & 1) != 0
        pkt['always'] = ((argheader >> 6) & 1) != 0
        return pkt
        
    elif lCommand == SVC_SOUND:
        pkt['channel'] = NETWORK_ReadUByte(stream)
        pkt['sound'] = NETWORK_ReadString(stream)
        pkt['volume'] = NETWORK_ReadUByte(stream)
        pkt['attenuation'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SOUNDACTOR or lCommand == SVC_SOUNDACTORIFNOTPLAYING:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['channel'] = NETWORK_ReadUShort(stream)
        pkt['sound'] = NETWORK_ReadString(stream)
        pkt['volume'] = NETWORK_ReadUByte(stream)
        pkt['attenuation'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SOUNDPOINT:
        pkt['position'] = [float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream)),
                           float(NETWORK_ReadShort(stream))]
        pkt['channel'] = NETWORK_ReadUByte(stream)
        pkt['sound'] = NETWORK_ReadString(stream)
        pkt['volume'] = NETWORK_ReadUByte(stream)
        pkt['attenuation'] = NETWORK_ReadUByte(stream)
        return pkt

    elif lCommand == SVC_STARTSECTORSEQUENCE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['channel'] = NETWORK_ReadUByte(stream)
        pkt['sequence'] = NETWORK_ReadString(stream)
        pkt['modenum'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_STOPSECTORSEQUENCE:
        pkt['sector'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CALLVOTE:
        pkt['caller'] = NETWORK_ReadUByte(stream)
        pkt['command'] = NETWORK_ReadString(stream)
        pkt['parameters'] = NETWORK_ReadString(stream)
        pkt['reason'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_PLAYERVOTE:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['vote'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_VOTEENDED:
        pkt['passed'] = NETWORK_ReadUByte(stream) != 0
        return pkt
        
    elif lCommand == SVC_MAPLOAD:
        pkt['map'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_MAPNEW:
        pkt['map'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_MAPEXIT:
        pkt['pos'] = NETWORK_ReadUByte(stream)
        pkt['nextmap'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_MAPAUTHENTICATE:
        pkt['map'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_SETMAPTIME:
        pkt['tics'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_SETMAPNUMKILLEDMONSTERS or\
         lCommand == SVC_SETMAPNUMFOUNDITEMS or\
         lCommand == SVC_SETMAPNUMFOUNDSECRETS or\
         lCommand == SVC_SETMAPNUMTOTALMONSTERS or\
         lCommand == SVC_SETMAPNUMTOTALITEMS:
        pkt['num'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETMAPMUSIC:
        pkt['music'] = NETWORK_ReadString(stream)
        pkt['order'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETMAPSKY:
        pkt['sky1'] = NETWORK_ReadString(stream)
        pkt['sky2'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_GIVEINVENTORY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemtype'] = NETWORK_ReadUShort(stream)
        pkt['amount'] = NETWORK_ReadShort(stream)
        return pkt
    
    elif lCommand == SVC_TAKEINVENTORY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemname'] = NETWORK_ReadString(stream)
        pkt['amount'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_GIVEPOWERUP:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemtype'] = NETWORK_ReadUShort(stream)
        pkt['amount'] = NETWORK_ReadShort(stream)
        pkt['ticsleft'] = NETWORK_ReadShort(stream)
        return pkt
    
    elif lCommand == SVC_DOINVENTORYPICKUP:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['itemname'] = NETWORK_ReadString(stream)
        pkt['pickupmessage'] = NETWORK_ReadString(stream)
        return pkt
    
    elif lCommand == SVC_DESTROYALLINVENTORY:
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DODOOR:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['direction'] = NETWORK_ReadUByte(stream)
        pkt['lighttag'] = NETWORK_ReadShort(stream)
        pkt['doorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYDOOR:
        pkt['doorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CHANGEDOORDIRECTION:
        pkt['doorid'] = NETWORK_ReadShort(stream)
        pkt['direction'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DOFLOOR:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['direction'] = NETWORK_ReadUByte(stream)
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['floordestdist'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['hexencrush'] = NETWORK_ReadUByte(stream) != 0
        pkt['floorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYFLOOR:
        pkt['floorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CHANGEFLOORDIRECTION:
        pkt['floorid'] = NETWORK_ReadShort(stream)
        pkt['direction'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_CHANGEFLOORTYPE:
        pkt['floorid'] = NETWORK_ReadShort(stream)
        pkt['type'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_CHANGEFLOORDESTDIST:
        pkt['floorid'] = NETWORK_ReadShort(stream)
        pkt['floordestdist'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_DOCEILING:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['direction'] = NETWORK_ReadUByte(stream)
        pkt['bottomheight'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['topheight'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['crush'] = NETWORK_ReadByte(stream)
        pkt['hexencrush'] = NETWORK_ReadUByte(stream) != 0
        pkt['silent'] = NETWORK_ReadShort(stream)
        pkt['ceilingid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYCEILING:
        pkt['ceilingid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CHANGECEILINGDIRECTION:
        pkt['ceilingid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CHANGECEILINGSPEED:
        pkt['ceilingid'] = NETWORK_ReadShort(stream)
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_PLAYCEILINGSOUND:
        pkt['ceilingid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOPLAT:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['status'] = NETWORK_ReadUByte(stream)
        pkt['high'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['low'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['platid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYPLAT:
        pkt['platid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_CHANGEPLATSTATUS:
        pkt['platid'] = NETWORK_ReadShort(stream)
        pkt['status'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_PLAYPLATSOUND:
        pkt['platid'] = NETWORK_ReadShort(stream)
        pkt['soundtype'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_DOELEVATOR:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['direction'] = NETWORK_ReadUByte(stream)
        pkt['floordestdist'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['ceilingdestdist'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['elevatorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYELEVATOR:
        pkt['elevatorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_STARTELEVATORSOUND:
        pkt['elevatorid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOPILLAR:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['floorspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['ceilingspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['floortarget'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['ceilingtarget'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['crush'] = NETWORK_ReadByte(stream)
        pkt['hexencrush'] = NETWORK_ReadUByte(stream) != 0
        pkt['pillarid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYPILLAR:
        pkt['pillarid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOWAGGLE:
        pkt['ceiling'] = NETWORK_ReadUByte(stream) != 0
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['originaldistance'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['accumulator'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['accelerationdelta'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['targetscale'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['scale'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['scaledelta'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['ticker'] = NETWORK_ReadLong(stream)
        pkt['state'] = NETWORK_ReadUByte(stream)
        pkt['waggleid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYWAGGLE:
        pkt['waggleid'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_UPDATEWAGGLE:
        pkt['waggleid'] = NETWORK_ReadShort(stream)
        pkt['accumulator'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
    
    elif lCommand == SVC_DOROTATEPOLY:
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYROTATEPOLY:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOMOVEPOLY:
        pkt['xspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['yspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYMOVEPOLY:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DOPOLYDOOR:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['xspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['yspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_DESTROYPOLYDOOR:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETPOLYDOORSPEEDPOSITION:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        pkt['xspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['yspeed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['x'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['y'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETPOLYDOORSPEEDROTATION:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['angle'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_PLAYPOLYOBJSOUND:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        pkt['polymode'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETPOLYOBJPOSITION:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        pkt['x'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['y'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        return pkt
        
    elif lCommand == SVC_SETPOLYOBJROTATION:
        pkt['polynum'] = NETWORK_ReadShort(stream)
        pkt['angle'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_EARTHQUAKE:
        pkt['netid'] = NETWORK_ReadShort(stream)
        pkt['intensity'] = NETWORK_ReadUByte(stream)
        pkt['duration'] = NETWORK_ReadShort(stream)
        pkt['tremrad'] = NETWORK_ReadShort(stream)
        pkt['quakesound'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_SETQUEUEPOSITION:
        pkt['position'] = NETWORK_ReadByte(stream)
        return pkt
        
    elif lCommand == SVC_DOSCROLLER or\
         lCommand == SVC_SETSCROLLER:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['dx'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['dy'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        if lCommand == SVC_DOSCROLLER:
            pkt['affectee'] = NETWORK_ReadShort(stream)
        else:
            pkt['tag'] = NETWORK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_SETWALLSCROLLER:
        pkt['scrollerid'] = NETWORK_ReadLong(stream)
        pkt['side'] = NETWORK_ReadUByte(stream)
        pkt['dx'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['dy'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['where'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_DOFLASHFADER:
        pkt['rgb1'] = [NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream)]
        pkt['rgb2'] = [NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream),
                       NETWORK_ReadFloat(stream)]
        pkt['time'] = NETWORK_ReadFloat(stream)
        pkt['player'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_GENERICCHEAT:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['cheat'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETCAMERATOTEXTURE:
        pkt['camera_netid'] = NETWORK_ReadShort(stream)
        pkt['texture'] = NETWORK_ReadString(stream)
        pkt['fov'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_CREATETRANSLATION or lCommand == SVC_CREATETRANSLATION2:
        pkt['idx'] = NETWORK_ReadShort(stream)
        pkt['edited'] = NETWORK_ReadUByte(stream) != 0
        pkt['start'] = NETWORK_ReadUByte(stream)
        pkt['end'] = NETWORK_ReadUByte(stream)
        if lCommand == SVC_CREATETRANSLATION:
            pkt['pal1'] = NETWORK_ReadUByte(stream)
            pkt['pal2'] = NETWORK_ReadUByte(stream)
        else:
            pkt['rgb1'] = (NETWORK_ReadUByte(stream) << 16) | (NETWORK_ReadUByte(stream) << 8) | (NETWORK_ReadUByte(stream))
            pkt['rgb2'] = (NETWORK_ReadUByte(stream) << 16) | (NETWORK_ReadUByte(stream) << 8) | (NETWORK_ReadUByte(stream))
        return pkt
        
    elif lCommand == SVC_REPLACETEXTURES:
        pkt['fromname'] = NETWORK_ReadLong(stream)
        pkt['toname'] = NETWORK_ReadLong(stream)
        pkt['texflags'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_SETSECTORLINK:
        pkt['sector'] = NETWORK_ReadShort(stream)
        pkt['args'] = [NETWORK_ReadUShort(stream), NETWORK_ReadUByte(stream), NETWORK_ReadUByte(stream)]
        return pkt
        
    elif lCommand == SVC_DOPUSHER:
        pkt['type'] = NETWORK_ReadUByte(stream)
        pkt['line'] = NETWORK_ReadShort(stream)
        pkt['magnitude'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['angle'] = NETWORK_ReadLong(stream)
        pkt['source_netid'] = NETWORK_ReadShort(stream)
        pkt['affectee'] = NETWRK_ReadShort(stream)
        return pkt
        
    elif lCommand == SVC_ADJUSTPUSHER:
        pkt['tag'] = NETWORK_ReadShort(stream)
        pkt['magnitude'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
        pkt['angle'] = NETWORK_ReadLong(stream)
        pkt['type'] = NETWORK_ReadUByte(stream)
        return pkt
        
    elif lCommand == SVC_IGNOREPLAYER:
        pkt['player'] = NETWORK_ReadUByte(stream)
        pkt['ticks'] = NETWORK_ReadLong(stream)
        return pkt
        
    elif lCommand == SVC_ANNOUNCERSOUND:
        pkt['entry'] = NETWORK_ReadString(stream)
        return pkt
        
    elif lCommand == SVC_EXTENDEDCOMMAND:
        lExtCommand = NETWORK_ReadUByte(stream)
        pkt['ext_name'] = enums.to_string(enums212, lExtCommand, ['SVC2_'])
        pkt['ext_id'] = lExtCommand
        
        if lExtCommand == SVC2_SETINVENTORYICON:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['itemtype'] = NETWORK_ReadUShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_FULLUPDATECOMPLETED:
            return pkt
            
        elif lExtCommand == SVC2_SETIGNOREWEAPONSELECT:
            pkt['ignoreweaponselect'] = NETWORK_ReadUByte(stream) != 0
            return pkt
            
        elif lExtCommand == SVC2_CLEARCONSOLEPLAYERWEAPON:
            return pkt
            
        elif lExtCommand == SVC2_LIGHTNING:
            return pkt
            
        elif lExtCommand == SVC2_CANCELFADE:
            pkt['player'] = NETWORK_ReadUByte(stream)
            return pkt
            
        elif lExtCommand == SVC2_PLAYBOUNCESOUND:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['onfloor'] = NETWORK_ReadUByte(stream) != 0
            return pkt
            
        elif lExtCommand == SVC2_GIVEWEAPONHOLDER:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['piecemask'] = NETWORK_ReadUShort(stream)
            pkt['piecetype'] = NETWORK_ReadUShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_SETHEXENARMORSLOTS:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['slots'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                            FIXED2FLOAT(NETWORK_ReadLong(stream)),
                            FIXED2FLOAT(NETWORK_ReadLong(stream)),
                            FIXED2FLOAT(NETWORK_ReadLong(stream)),
                            FIXED2FLOAT(NETWORK_ReadLong(stream))]
            return pkt
            
        elif lExtCommand == SVC2_SETTHINGREACTIONTIME:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['reactiontime'] = NETWORK_ReadShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_SETFASTCHASESTRAFECOUNT:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['strafecount'] = NETWORK_ReadUByte(stream)
            return pkt
            
        elif lExtCommand == SVC2_RESETMAP:
            return pkt
            
        elif lExtCommand == SVC2_SETPOWERUPBLENDCOLOR:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['itemtype'] = NETWORK_ReadUShort(stream)
            pkt['blendcolor'] = NETWORK_ReadULong(stream)
            return pkt
            
        elif lExtCommand == SVC2_SETPLAYERHAZARDCOUNT:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['hazardcount'] = NETWORK_ReadShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_SCROLL3DMIDTEX:
            pkt['sector'] = NETWORK_ReadUByte(stream) # wtf? probably some underdeveloped command
            pkt['move'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
            pkt['ceiling'] = NETWORK_ReadUByte(stream) != 0
            return pkt
            
        elif lExtCommand == SVC2_SETPLAYERLOGNUMBER:
            pkt['player'] = NETWORK_ReadUByte(stream)
            pkt['lognumber'] = NETWORK_ReadShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_SETTHINGSPECIAL:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['special'] = NETWORK_ReadUShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_SYNCPATHFOLLOWER:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['currnodeid'] = NETWORK_ReadShort(stream)
            pkt['prevnodeid'] = NETWORK_ReadShort(stream)
            pkt['servertime'] = NETWORK_ReadFloat(stream)
            return pkt
            
        elif lExtCommand == SVC2_SRP_USER_START_AUTHENTICATION or\
             lExtCommand == SVC2_SRP_USER_PROCESS_CHALLENGE or\
             lExtCommand == SVC2_SRP_USER_VERIFY_SESSION:
            CLIENT_ProcessSRPServerCommand(pkt, lExtCommand, stream)
            return pkt
            
        elif lExtCommand == SVC2_SETTHINGHEALTH:
            pkt['netid'] = NETWORK_ReadShort(stream)
            pkt['health'] = NETWORK_ReadByte(stream)
            return pkt
            
        elif lExtCommand == SVC2_SETCVAR:
            pkt['name'] = NETWORK_ReadString(stream)
            pkt['value'] = NETWORK_ReadString(stream)
            return pkt
            
        elif lExtCommand == SVC2_STOPPOLYOBJSOUND:
            pkt['polynum'] = NETWORK_ReadShort(stream)
            return pkt
            
        elif lExtCommand == SVC2_BUILDSTAIR:
            pkt['type'] = NETWORK_ReadUByte(stream)
            pkt['sector'] = NETWORK_ReadShort(stream)
            pkt['direction'] = NETWORK_ReadByte(stream)
            pkt['speed'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
            pkt['floordestdist'] = FIXED2FLOAT(NETWORK_ReadLong(stream))
            pkt['crush'] = NETWORK_ReadByte(stream)
            pkt['hexencrush'] = NETWORK_ReadUByte(stream) != 0
            pkt['resetcount'] = NETWORK_ReadLong(stream)
            pkt['delay'] = NETWORK_ReadLong(stream)
            pkt['pausetime'] = NETWORK_ReadLong(stream)
            pkt['steptime'] = NETWORK_ReadLong(stream)
            pkt['persteptime'] = NETWORK_ReadLong(stream)
            pkt['floorid'] = NETWORK_ReadShort(stream)
            return pkt

            
    
###########################################
# version specific   ######################

def CLIENTDEMO_ReadUserInfo(stream):
    return {'name': NETWORK_ReadString(stream),
            'gender': NETWORK_ReadUByte(stream),
            'color': NETWORK_ReadULong(stream),
            'aimdist': NETWORK_ReadLong(stream),
            'skin': NETWORK_ReadString(stream),
            'rail_color': NETWORK_ReadULong(stream),
            'handicap': NETWORK_ReadUByte(stream),
            'ticsperupdate': NETWORK_ReadUByte(stream),
            'connectiontype': NETWORK_ReadUByte(stream),
            'clientflags': NETWORK_ReadUByte(stream),
            'playerclass': NETWORK_ReadString(stream)}

def CLIENTDEMO_ReadTiccmd(stream):
    cmd = {}
    cmd['yaw'] = NETWORK_ReadShort(stream)
    cmd['roll'] = NETWORK_ReadShort(stream)
    cmd['pitch'] = NETWORK_ReadShort(stream)
    cmd['buttons'] = NETWORK_ReadUByte(stream)
    cmd['upmove'] = NETWORK_ReadShort(stream)
    cmd['forwardmove'] = NETWORK_ReadShort(stream)
    cmd['sidemove'] = NETWORK_ReadShort(stream)
    return cmd
    
def client_SpawnPlayer(pkt, stream, bMorph):
    pkt['morph'] = bMorph
    pkt['player'] = NETWORK_ReadUByte(stream)
    pkt['state_old'] = NETWORK_ReadUByte(stream)
    pkt['bot'] = NETWORK_ReadUByte(stream) != 0
    pkt['state'] = NETWORK_ReadUByte(stream)
    pkt['spectating'] = NETWORK_ReadUByte(stream) != 0
    pkt['spectating_dead'] = NETWORK_ReadUByte(stream) != 0
    pkt['body_netid'] = NETWORK_ReadShort(stream)
    pkt['angle'] = NETWORK_ReadLong(stream)
    pkt['position'] = [FIXED2FLOAT(NETWORK_ReadLong(stream)),
                       FIXED2FLOAT(NETWORK_ReadLong(stream)),
                       FIXED2FLOAT(NETWORK_ReadLong(stream))]
    pkt['class'] = NETWORK_ReadShort(stream)
    if bMorph:
        pkt['morph_netid'] = NETWORK_ReadShort(stream)

def CLIENT_ProcessSRPServerCommand(pkt, lCommand, stream):
    if lCommand == SVC2_SRP_USER_START_AUTHENTICATION:
        pkt['username'] = NETWORK_ReadString(stream)
    elif lCommand == SVC2_SRP_USER_PROCESS_CHALLENGE:
        lensalt = NETWORK_ReadUByte(stream)
        salt = []
        for i in range(lensalt):
            salt.append(NETWORK_ReadUByte(stream))
        pkt['salt'] = salt
        lenb = NETWORK_ReadUShort(stream)
        bytesb = []
        for i in range(lenb):
            bytesb.append(NETWORK_ReadUByte(stream))
        pkt['bytesb'] = bytesb
    elif lCommand == SVC2_SRP_USER_VERIFY_SESSION:
        lenhamk = NETWORK_ReadUShort(stream)
        byteshamk = []
        for i in range(lenhamk):
            byteshamk.append(NETWORK_ReadUByte(stream))
        pkt['byteshamk'] = byteshamk

