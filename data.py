# -*- coding: utf-8 -*-

class UserInfo:
    def __init__(self):
        self.netname = None
        self.gender = 0
        self.color = 0x00FF00
        self.aimdist = 5000
        self.skin = ''
        self.lRailgunTrailColor = 0x0000FF
        self.lHandicap = 0
        self.ulTicsPerUpdate = 1
        self.ulConnectionType = 0
        self.clientFlags = 0
        self.PlayerClass = 'DoomPlayer'
        
class Player:
    def __init__(self):
        self.userinfo = UserInfo()
        self.ingame = False
        
MAXPLAYERS = 64
players = []
consoleplayer = -1

def CLIENT_ClearAllPlayers():
    global consoleplayer
    del players[:]
    for i in range(MAXPLAYERS):
        players.append(Player())
    consoleplayer = 0
    
CLIENT_ClearAllPlayers()

def V_ColorizeString(instr):
    outstr = ''
    i = -1
    while i+1 < len(instr):
        i += 1
        c = instr[i]
        if c == '\\' and i+1 < len(instr):
            outstr += '\034'
            i += 1
            continue
        outstr += c
    return outstr        

def V_CleanPlayerName(instr):
    outstr = ''
    i = -1
    in_color = False
    in_ccolor = False
    while i+1 < len(instr):
        i += 1
        c = instr[i]
        if in_ccolor:
            if c == ']':
                in_ccolor = False
        elif in_color:
            in_color = False
            if c == '[':
                in_ccolor = True
        elif c == '\034': # \c
            in_color = True
            in_ccolor = False
        else:
            outstr += c
    return outstr
    
def FIXED2FLOAT(f):
    return float(f) / 65536
    
def FLOAT2FIXED(f):
    return int(f * 65536)

class Struct:
    def __init__(self, **entries):
        self.keys = []
        for k in entries:
            self.keys.append(k)
        self.__dict__.update(entries)
        
    def __repr__(self):
        outdic = {}
        for k in self.keys:
            outdic[k] = getattr(self, k)
        return repr(outdic)
