# -*- coding: utf-8 -*-

from enums import *


BEGIN_ENUM ( 'SVCC' )
ENUM_ELEMENT ( 'SVCC_AUTHENTICATE' )
ENUM_ELEMENT ( 'SVCC_MAPLOAD' )
ENUM_ELEMENT ( 'SVCC_ERROR' )
ENUM_ELEMENT ( 'NUM_SERVERCONNECT_COMMANDS' )
END_ENUM ( 'SVCC' )


BEGIN_ENUM ( 'SVC' )
ENUM_ELEMENT2 ( 'SVC_HEADER', NUM_SERVERCONNECT_COMMANDS )    # GENERAL PROTOCOL COMMANDS
ENUM_ELEMENT ( 'SVC_UNRELIABLEPACKET' )
ENUM_ELEMENT ( 'SVC_PING' )
ENUM_ELEMENT ( 'SVC_NOTHING' )
ENUM_ELEMENT ( 'SVC_BEGINSNAPSHOT' )
ENUM_ELEMENT ( 'SVC_ENDSNAPSHOT' )
ENUM_ELEMENT ( 'SVC_SPAWNPLAYER' )                    # PLAYER COMMANDS
ENUM_ELEMENT ( 'SVC_SPAWNMORPHPLAYER' )
ENUM_ELEMENT ( 'SVC_MOVEPLAYER' )
ENUM_ELEMENT ( 'SVC_DAMAGEPLAYER' )
ENUM_ELEMENT ( 'SVC_KILLPLAYER' )
ENUM_ELEMENT ( 'SVC_SETPLAYERHEALTH' )
ENUM_ELEMENT ( 'SVC_SETPLAYERARMOR' )
ENUM_ELEMENT ( 'SVC_SETPLAYERSTATE' )
ENUM_ELEMENT ( 'SVC_SETPLAYERUSERINFO' )
ENUM_ELEMENT ( 'SVC_SETPLAYERFRAGS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERPOINTS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERWINS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERKILLCOUNT' )
ENUM_ELEMENT ( 'SVC_SETPLAYERCHATSTATUS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERCONSOLESTATUS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERLAGGINGSTATUS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERREADYTOGOONSTATUS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERTEAM' )
ENUM_ELEMENT ( 'SVC_SETPLAYERCAMERA' )
ENUM_ELEMENT ( 'SVC_SETPLAYERPOISONCOUNT' )
ENUM_ELEMENT ( 'SVC_SETPLAYERAMMOCAPACITY' )
ENUM_ELEMENT ( 'SVC_SETPLAYERCHEATS' )
ENUM_ELEMENT ( 'SVC_SETPLAYERPENDINGWEAPON' )
ENUM_ELEMENT ( 'SVC_SETPLAYERPIECES' )
ENUM_ELEMENT ( 'SVC_SETPLAYERPSPRITE' )
ENUM_ELEMENT ( 'SVC_SETPLAYERBLEND' )
ENUM_ELEMENT ( 'SVC_SETPLAYERMAXHEALTH' )
ENUM_ELEMENT ( 'SVC_SETPLAYERLIVESLEFT' )
ENUM_ELEMENT ( 'SVC_UPDATEPLAYERPING' )
ENUM_ELEMENT ( 'SVC_UPDATEPLAYEREXTRADATA' )
ENUM_ELEMENT ( 'SVC_UPDATEPLAYERTIME' )
ENUM_ELEMENT ( 'SVC_MOVELOCALPLAYER' )
ENUM_ELEMENT ( 'SVC_DISCONNECTPLAYER' )
ENUM_ELEMENT ( 'SVC_SETCONSOLEPLAYER' )
ENUM_ELEMENT ( 'SVC_CONSOLEPLAYERKICKED' )
ENUM_ELEMENT ( 'SVC_GIVEPLAYERMEDAL' )
ENUM_ELEMENT ( 'SVC_RESETALLPLAYERSFRAGCOUNT' )
ENUM_ELEMENT ( 'SVC_PLAYERISSPECTATOR' )
ENUM_ELEMENT ( 'SVC_PLAYERSAY' )
ENUM_ELEMENT ( 'SVC_PLAYERTAUNT' )
ENUM_ELEMENT ( 'SVC_PLAYERRESPAWNINVULNERABILITY' )
ENUM_ELEMENT ( 'SVC_PLAYERUSEINVENTORY' )
ENUM_ELEMENT ( 'SVC_PLAYERDROPINVENTORY' )
ENUM_ELEMENT ( 'SVC_SPAWNTHING' )                        # THING COMMANDS
ENUM_ELEMENT ( 'SVC_SPAWNTHINGNONETID' )
ENUM_ELEMENT ( 'SVC_SPAWNTHINGEXACT' )
ENUM_ELEMENT ( 'SVC_SPAWNTHINGEXACTNONETID' )
ENUM_ELEMENT ( 'SVC_MOVETHING' )
ENUM_ELEMENT ( 'SVC_MOVETHINGEXACT' )
ENUM_ELEMENT ( 'SVC_DAMAGETHING' )
ENUM_ELEMENT ( 'SVC_KILLTHING' )
ENUM_ELEMENT ( 'SVC_SETTHINGSTATE' )
ENUM_ELEMENT ( 'SVC_SETTHINGTARGET' )
ENUM_ELEMENT ( 'SVC_DESTROYTHING' )
ENUM_ELEMENT ( 'SVC_SETTHINGANGLE' )
ENUM_ELEMENT ( 'SVC_SETTHINGANGLEEXACT' )
ENUM_ELEMENT ( 'SVC_SETTHINGWATERLEVEL' )
ENUM_ELEMENT ( 'SVC_SETTHINGFLAGS' )
ENUM_ELEMENT ( 'SVC_SETTHINGARGUMENTS' )
ENUM_ELEMENT ( 'SVC_SETTHINGTRANSLATION' )
ENUM_ELEMENT ( 'SVC_SETTHINGPROPERTY' )
ENUM_ELEMENT ( 'SVC_SETTHINGSOUND' )
ENUM_ELEMENT ( 'SVC_SETTHINGSPAWNPOINT' )
ENUM_ELEMENT ( 'SVC_SETTHINGSPECIAL1' )
ENUM_ELEMENT ( 'SVC_SETTHINGSPECIAL2' )
ENUM_ELEMENT ( 'SVC_SETTHINGTICS' )
ENUM_ELEMENT ( 'SVC_SETTHINGTID' )
ENUM_ELEMENT ( 'SVC_SETTHINGGRAVITY' )
ENUM_ELEMENT ( 'SVC_SETTHINGFRAME' )
ENUM_ELEMENT ( 'SVC_SETTHINGFRAMENF' )
ENUM_ELEMENT ( 'SVC_SETWEAPONAMMOGIVE' )
ENUM_ELEMENT ( 'SVC_THINGISCORPSE' )
ENUM_ELEMENT ( 'SVC_HIDETHING' )
ENUM_ELEMENT ( 'SVC_TELEPORTTHING' )
ENUM_ELEMENT ( 'SVC_THINGACTIVATE' )
ENUM_ELEMENT ( 'SVC_THINGDEACTIVATE' )
ENUM_ELEMENT ( 'SVC_RESPAWNDOOMTHING' )
ENUM_ELEMENT ( 'SVC_RESPAWNRAVENTHING' )
ENUM_ELEMENT ( 'SVC_SPAWNBLOOD' )
ENUM_ELEMENT ( 'SVC_SPAWNPUFF' )
ENUM_ELEMENT ( 'SVC_PRINT' )                            # PRINT COMMANDS
ENUM_ELEMENT ( 'SVC_PRINTMID' )
ENUM_ELEMENT ( 'SVC_PRINTMOTD' )
ENUM_ELEMENT ( 'SVC_PRINTHUDMESSAGE' )
ENUM_ELEMENT ( 'SVC_PRINTHUDMESSAGEFADEOUT' )
ENUM_ELEMENT ( 'SVC_PRINTHUDMESSAGEFADEINOUT' )
ENUM_ELEMENT ( 'SVC_PRINTHUDMESSAGETYPEONFADEOUT' )
ENUM_ELEMENT ( 'SVC_SETGAMEMODE' )                    # GAME COMMANDS
ENUM_ELEMENT ( 'SVC_SETGAMESKILL' )
ENUM_ELEMENT ( 'SVC_SETGAMEDMFLAGS' )
ENUM_ELEMENT ( 'SVC_SETGAMEMODELIMITS' )
ENUM_ELEMENT ( 'SVC_SETGAMEENDLEVELDELAY' )
ENUM_ELEMENT ( 'SVC_SETGAMEMODESTATE' )
ENUM_ELEMENT ( 'SVC_SETDUELNUMDUELS' )
ENUM_ELEMENT ( 'SVC_SETLMSSPECTATORSETTINGS' )
ENUM_ELEMENT ( 'SVC_SETLMSALLOWEDWEAPONS' )
ENUM_ELEMENT ( 'SVC_SETINVASIONNUMMONSTERSLEFT' )
ENUM_ELEMENT ( 'SVC_SETINVASIONWAVE' )
ENUM_ELEMENT ( 'SVC_SETSIMPLECTFSTMODE' )
ENUM_ELEMENT ( 'SVC_DOPOSSESSIONARTIFACTPICKEDUP' )
ENUM_ELEMENT ( 'SVC_DOPOSSESSIONARTIFACTDROPPED' )
ENUM_ELEMENT ( 'SVC_DOGAMEMODEFIGHT' )
ENUM_ELEMENT ( 'SVC_DOGAMEMODECOUNTDOWN' )
ENUM_ELEMENT ( 'SVC_DOGAMEMODEWINSEQUENCE' )
ENUM_ELEMENT ( 'SVC_SETDOMINATIONSTATE' )
ENUM_ELEMENT ( 'SVC_SETDOMINATIONPOINTOWNER' )
ENUM_ELEMENT ( 'SVC_SETTEAMFRAGS' )                    # TEAM COMMANDS
ENUM_ELEMENT ( 'SVC_SETTEAMSCORE' )
ENUM_ELEMENT ( 'SVC_SETTEAMWINS' )
ENUM_ELEMENT ( 'SVC_SETTEAMRETURNTICKS' )
ENUM_ELEMENT ( 'SVC_TEAMFLAGRETURNED' )
ENUM_ELEMENT ( 'SVC_TEAMFLAGDROPPED' )
ENUM_ELEMENT ( 'SVC_SPAWNMISSILE' )                    # MISSILE COMMANDS
ENUM_ELEMENT ( 'SVC_SPAWNMISSILEEXACT' )
ENUM_ELEMENT ( 'SVC_MISSILEEXPLODE' )
ENUM_ELEMENT ( 'SVC_WEAPONSOUND' )                    # WEAPON COMMANDS
ENUM_ELEMENT ( 'SVC_WEAPONCHANGE' )
ENUM_ELEMENT ( 'SVC_WEAPONRAILGUN' )
ENUM_ELEMENT ( 'SVC_SETSECTORFLOORPLANE' )            # SECTOR COMMANDS
ENUM_ELEMENT ( 'SVC_SETSECTORCEILINGPLANE' )
ENUM_ELEMENT ( 'SVC_SETSECTORFLOORPLANESLOPE' )
ENUM_ELEMENT ( 'SVC_SETSECTORCEILINGPLANESLOPE' )
ENUM_ELEMENT ( 'SVC_SETSECTORLIGHTLEVEL' )
ENUM_ELEMENT ( 'SVC_SETSECTORCOLOR' )
ENUM_ELEMENT ( 'SVC_SETSECTORCOLORBYTAG' )
ENUM_ELEMENT ( 'SVC_SETSECTORFADE' )
ENUM_ELEMENT ( 'SVC_SETSECTORFADEBYTAG' )
ENUM_ELEMENT ( 'SVC_SETSECTORFLAT' )
ENUM_ELEMENT ( 'SVC_SETSECTORPANNING' )
ENUM_ELEMENT ( 'SVC_SETSECTORROTATION' )
ENUM_ELEMENT ( 'SVC_SETSECTORROTATIONBYTAG' )
ENUM_ELEMENT ( 'SVC_SETSECTORSCALE' )
ENUM_ELEMENT ( 'SVC_SETSECTORSPECIAL' )
ENUM_ELEMENT ( 'SVC_SETSECTORFRICTION' )
ENUM_ELEMENT ( 'SVC_SETSECTORANGLEYOFFSET' )
ENUM_ELEMENT ( 'SVC_SETSECTORGRAVITY' )
ENUM_ELEMENT ( 'SVC_SETSECTORREFLECTION' )
ENUM_ELEMENT ( 'SVC_STOPSECTORLIGHTEFFECT' )
ENUM_ELEMENT ( 'SVC_DESTROYALLSECTORMOVERS' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTFIREFLICKER' )        # SECTOR LIGHT COMMANDS
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTFLICKER' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTLIGHTFLASH' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTSTROBE' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTGLOW' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTGLOW2' )
ENUM_ELEMENT ( 'SVC_DOSECTORLIGHTPHASED' )
ENUM_ELEMENT ( 'SVC_SETLINEALPHA' )                    # LINE COMMANDS
ENUM_ELEMENT ( 'SVC_SETLINETEXTURE' )
ENUM_ELEMENT ( 'SVC_SETLINETEXTUREBYID' )
ENUM_ELEMENT ( 'SVC_SETSOMELINEFLAGS' )
ENUM_ELEMENT ( 'SVC_SETSIDEFLAGS' )                    # SIDE COMMANDS
ENUM_ELEMENT ( 'SVC_ACSSCRIPTEXECUTE' )                # ACS COMMANDS
ENUM_ELEMENT ( 'SVC_SOUND' )                            # SOUND COMMANDS
ENUM_ELEMENT ( 'SVC_SOUNDACTOR' )
ENUM_ELEMENT ( 'SVC_SOUNDACTORIFNOTPLAYING' )
ENUM_ELEMENT ( 'SVC_SOUNDPOINT' )
ENUM_ELEMENT ( 'SVC_STARTSECTORSEQUENCE' )            # SECTOR SEQUENCE COMMANDS
ENUM_ELEMENT ( 'SVC_STOPSECTORSEQUENCE' )
ENUM_ELEMENT ( 'SVC_CALLVOTE' )                        # VOTING COMMANDS
ENUM_ELEMENT ( 'SVC_PLAYERVOTE' )
ENUM_ELEMENT ( 'SVC_VOTEENDED' )
ENUM_ELEMENT ( 'SVC_MAPLOAD' )                        # MAP COMMANDS
ENUM_ELEMENT ( 'SVC_MAPNEW' )
ENUM_ELEMENT ( 'SVC_MAPEXIT' )
ENUM_ELEMENT ( 'SVC_MAPAUTHENTICATE' )
ENUM_ELEMENT ( 'SVC_SETMAPTIME' )
ENUM_ELEMENT ( 'SVC_SETMAPNUMKILLEDMONSTERS' )
ENUM_ELEMENT ( 'SVC_SETMAPNUMFOUNDITEMS' )
ENUM_ELEMENT ( 'SVC_SETMAPNUMFOUNDSECRETS' )
ENUM_ELEMENT ( 'SVC_SETMAPNUMTOTALMONSTERS' )
ENUM_ELEMENT ( 'SVC_SETMAPNUMTOTALITEMS' )
ENUM_ELEMENT ( 'SVC_SETMAPMUSIC' )
ENUM_ELEMENT ( 'SVC_SETMAPSKY' )
ENUM_ELEMENT ( 'SVC_GIVEINVENTORY' )                    # INVENTORY COMMANDS
ENUM_ELEMENT ( 'SVC_TAKEINVENTORY' )
ENUM_ELEMENT ( 'SVC_GIVEPOWERUP' )
ENUM_ELEMENT ( 'SVC_DOINVENTORYPICKUP' )
ENUM_ELEMENT ( 'SVC_DESTROYALLINVENTORY' )
ENUM_ELEMENT ( 'SVC_DODOOR' )                            # DOOR COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYDOOR' )
ENUM_ELEMENT ( 'SVC_CHANGEDOORDIRECTION' )
ENUM_ELEMENT ( 'SVC_DOFLOOR' )                        # FLOOR COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYFLOOR' )
ENUM_ELEMENT ( 'SVC_CHANGEFLOORDIRECTION' )
ENUM_ELEMENT ( 'SVC_CHANGEFLOORTYPE' )
ENUM_ELEMENT ( 'SVC_CHANGEFLOORDESTDIST' )
ENUM_ELEMENT ( 'SVC_STARTFLOORSOUND' )
ENUM_ELEMENT ( 'SVC_DOCEILING' )                        # CEILING COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYCEILING' )
ENUM_ELEMENT ( 'SVC_CHANGECEILINGDIRECTION' )
ENUM_ELEMENT ( 'SVC_CHANGECEILINGSPEED' )
ENUM_ELEMENT ( 'SVC_PLAYCEILINGSOUND' )
ENUM_ELEMENT ( 'SVC_DOPLAT' )                            # PLAT COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYPLAT' )
ENUM_ELEMENT ( 'SVC_CHANGEPLATSTATUS' )
ENUM_ELEMENT ( 'SVC_PLAYPLATSOUND' )
ENUM_ELEMENT ( 'SVC_DOELEVATOR' )                        # ELEVATOR COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYELEVATOR' )
ENUM_ELEMENT ( 'SVC_STARTELEVATORSOUND' )
ENUM_ELEMENT ( 'SVC_DOPILLAR' )                        # PILLAR COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYPILLAR' )
ENUM_ELEMENT ( 'SVC_DOWAGGLE' )                        # WAGGLE COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYWAGGLE' )
ENUM_ELEMENT ( 'SVC_UPDATEWAGGLE' )
ENUM_ELEMENT ( 'SVC_DOROTATEPOLY' )                    # ROTATEPOLY COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYROTATEPOLY' )
ENUM_ELEMENT ( 'SVC_DOMOVEPOLY' )                        # MOVEPOLY COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYMOVEPOLY' )
ENUM_ELEMENT ( 'SVC_DOPOLYDOOR' )                        # POLYDOOR COMMANDS
ENUM_ELEMENT ( 'SVC_DESTROYPOLYDOOR' )
ENUM_ELEMENT ( 'SVC_SETPOLYDOORSPEEDPOSITION' )
ENUM_ELEMENT ( 'SVC_SETPOLYDOORSPEEDROTATION' )
ENUM_ELEMENT ( 'SVC_PLAYPOLYOBJSOUND' )                # GENERIC POLYOBJECT COMMANDS
ENUM_ELEMENT ( 'SVC_SETPOLYOBJPOSITION' )
ENUM_ELEMENT ( 'SVC_SETPOLYOBJROTATION' )
ENUM_ELEMENT ( 'SVC_EARTHQUAKE' )                        # MISC. COMMANDS
ENUM_ELEMENT ( 'SVC_SETQUEUEPOSITION' )
ENUM_ELEMENT ( 'SVC_DOSCROLLER' )
ENUM_ELEMENT ( 'SVC_SETSCROLLER' )
ENUM_ELEMENT ( 'SVC_SETWALLSCROLLER' )
ENUM_ELEMENT ( 'SVC_DOFLASHFADER' )
ENUM_ELEMENT ( 'SVC_GENERICCHEAT' )
ENUM_ELEMENT ( 'SVC_SETCAMERATOTEXTURE' )
ENUM_ELEMENT ( 'SVC_CREATETRANSLATION' )
ENUM_ELEMENT ( 'SVC_IGNOREPLAYER' )
ENUM_ELEMENT ( 'SVC_SPAWNBLOODSPLATTER' )
ENUM_ELEMENT ( 'SVC_SPAWNBLOODSPLATTER2' )
ENUM_ELEMENT ( 'SVC_CREATETRANSLATION2' )
ENUM_ELEMENT ( 'SVC_REPLACETEXTURES' )
ENUM_ELEMENT ( 'SVC_SETSECTORLINK' )
ENUM_ELEMENT ( 'SVC_DOPUSHER' )
ENUM_ELEMENT ( 'SVC_ADJUSTPUSHER' )
ENUM_ELEMENT ( 'SVC_ANNOUNCERSOUND' )
ENUM_ELEMENT ( 'SVC_EXTENDEDCOMMAND' )
ENUM_ELEMENT ( 'NUM_SERVER_COMMANDS' )
END_ENUM ( 'SVC' )


BEGIN_ENUM ( 'SVC2' )
ENUM_ELEMENT ( 'SVC2_SETINVENTORYICON' )
ENUM_ELEMENT ( 'SVC2_FULLUPDATECOMPLETED' )
ENUM_ELEMENT ( 'SVC2_SETIGNOREWEAPONSELECT' )
ENUM_ELEMENT ( 'SVC2_CLEARCONSOLEPLAYERWEAPON' )
ENUM_ELEMENT ( 'SVC2_LIGHTNING' )
ENUM_ELEMENT ( 'SVC2_CANCELFADE' )
ENUM_ELEMENT ( 'SVC2_PLAYBOUNCESOUND' )
ENUM_ELEMENT ( 'SVC2_GIVEWEAPONHOLDER' )
ENUM_ELEMENT ( 'SVC2_SETHEXENARMORSLOTS' )
ENUM_ELEMENT ( 'SVC2_SETTHINGREACTIONTIME' )
ENUM_ELEMENT ( 'SVC2_SETFASTCHASESTRAFECOUNT' )
ENUM_ELEMENT ( 'SVC2_RESETMAP' )
ENUM_ELEMENT ( 'SVC2_SETPOWERUPBLENDCOLOR' )
ENUM_ELEMENT ( 'SVC2_SETPLAYERHAZARDCOUNT' )
ENUM_ELEMENT ( 'SVC2_SCROLL3DMIDTEX' )
ENUM_ELEMENT ( 'SVC2_SETPLAYERLOGNUMBER' )
ENUM_ELEMENT ( 'SVC2_SETTHINGSPECIAL' )
ENUM_ELEMENT ( 'SVC2_SYNCPATHFOLLOWER' )
ENUM_ELEMENT ( 'SVC2_SETTHINGHEALTH' )
ENUM_ELEMENT ( 'SVC2_SETCVAR' )
ENUM_ELEMENT ( 'SVC2_STOPPOLYOBJSOUND' )
ENUM_ELEMENT ( 'SVC2_BUILDSTAIR' )
# [BB] Commands necessary for the account system.
ENUM_ELEMENT ( 'SVC2_SRP_USER_START_AUTHENTICATION' )
ENUM_ELEMENT ( 'SVC2_SRP_USER_PROCESS_CHALLENGE' )
ENUM_ELEMENT ( 'SVC2_SRP_USER_VERIFY_SESSION' )
ENUM_ELEMENT ( 'NUM_SVC2_COMMANDS' )
END_ENUM ( 'SVC2' )


BEGIN_ENUM ( 'CLD' )
ENUM_ELEMENT2 ( 'CLD_DEMOLENGTH', NUM_SERVER_COMMANDS )
ENUM_ELEMENT ( 'CLD_DEMOVERSION' )
ENUM_ELEMENT ( 'CLD_CVARS' )
ENUM_ELEMENT ( 'CLD_USERINFO' )
ENUM_ELEMENT ( 'CLD_BODYSTART' )
ENUM_ELEMENT ( 'CLD_TICCMD' )
ENUM_ELEMENT ( 'CLD_LOCALCOMMAND' )
ENUM_ELEMENT ( 'CLD_DEMOEND' )
ENUM_ELEMENT ( 'CLD_DEMOWADS' )
ENUM_ELEMENT ( 'NUM_DEMO_COMMANDS' )
END_ENUM ( 'CLD' )


BEGIN_ENUM ( 'LCMD' )
ENUM_ELEMENT ( 'LCMD_INVUSE' )
ENUM_ELEMENT ( 'LCMD_CENTERVIEW' )
ENUM_ELEMENT ( 'LCMD_TAUNT' )
ENUM_ELEMENT ( 'LCMD_NOCLIP' )
END_ENUM ( 'LCMD' )


BEGIN_ENUM ( 'NETWORK_ERRORCODE' )
# Client has the wrong password.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_WRONGPASSWORD' )
# Client has the wrong version.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_WRONGVERSION' )
# Client is using a version with different network protocol.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_WRONGPROTOCOLVERSION' )
# Client has been banned.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_BANNED' )
# The server is full.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_SERVERISFULL' )
# Client has the wrong version of the current level.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_AUTHENTICATIONFAILED' )
# Client failed to send userinfo when connecting.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_FAILEDTOSENDUSERINFO' )
# [RC] Too many connections from the IP.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_TOOMANYCONNECTIONSFROMIP' )
# [BB] The protected lump authentication failed.
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_PROTECTED_LUMP_AUTHENTICATIONFAILED' )
# [TP] The client sent bad userinfo
ENUM_ELEMENT ( 'NETWORK_ERRORCODE_USERINFOREJECTED' )
ENUM_ELEMENT ( 'NUM_NETWORK_ERRORCODES' )
END_ENUM ( 'NETWORK_ERRORCODE' )


BEGIN_ENUM ( 'PLAYER' )
ENUM_ELEMENT2 ( 'PLAYER_VISIBLE', 1<<0 )
ENUM_ELEMENT2 ( 'PLAYER_ATTACK', 1<<1 )
ENUM_ELEMENT2 ( 'PLAYER_ALTATTACK', 1<<2 )
END_ENUM ( 'PLAYER' )


BEGIN_ENUM ( 'USERINFO' )
ENUM_ELEMENT2 ( 'USERINFO_NAME', 1 )
ENUM_ELEMENT2 ( 'USERINFO_GENDER', 2 )
ENUM_ELEMENT2 ( 'USERINFO_COLOR', 4 )
ENUM_ELEMENT2 ( 'USERINFO_AIMDISTANCE', 8 )
ENUM_ELEMENT2 ( 'USERINFO_SKIN', 16 )
ENUM_ELEMENT2 ( 'USERINFO_RAILCOLOR', 32 )
ENUM_ELEMENT2 ( 'USERINFO_HANDICAP', 64 )
ENUM_ELEMENT2 ( 'USERINFO_PLAYERCLASS', 128 )
ENUM_ELEMENT2 ( 'USERINFO_TICSPERUPDATE', 256 )
ENUM_ELEMENT2 ( 'USERINFO_CONNECTIONTYPE', 512 )
ENUM_ELEMENT2 ( 'USERINFO_CLIENTFLAGS', 1024 )
END_ENUM ( 'USERINFO' )


BEGIN_ENUM ( 'CM' )
ENUM_ELEMENT2 ( 'CM_X', 1 << 0 )
ENUM_ELEMENT2 ( 'CM_Y', 1 << 1 )
ENUM_ELEMENT2 ( 'CM_Z', 1 << 2 )
ENUM_ELEMENT2 ( 'CM_ANGLE', 1 << 3 )
ENUM_ELEMENT2 ( 'CM_MOMX', 1 << 4 )
ENUM_ELEMENT2 ( 'CM_MOMY', 1 << 5 )
ENUM_ELEMENT2 ( 'CM_MOMZ', 1 << 6 )
ENUM_ELEMENT2 ( 'CM_PITCH', 1 << 7 )
ENUM_ELEMENT2 ( 'CM_MOVEDIR', 1 << 8 )
ENUM_ELEMENT2 ( 'CM_REUSE_X', 1 << 9 )
ENUM_ELEMENT2 ( 'CM_REUSE_Y', 1 << 10 )
ENUM_ELEMENT2 ( 'CM_REUSE_Z', 1 << 11 )
ENUM_ELEMENT2 ( 'CM_LAST_X', 1 << 12 )
ENUM_ELEMENT2 ( 'CM_LAST_Y', 1 << 13 )
ENUM_ELEMENT2 ( 'CM_LAST_Z', 1 << 14 )
ENUM_ELEMENT2 ( 'CM_NOLAST', 1 << 15 )
END_ENUM ( 'CM' )


BEGIN_ENUM ( 'FLAGSET' )
ENUM_ELEMENT ( 'FLAGSET_UNKNOWN' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS2' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS3' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS4' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS5' )
ENUM_ELEMENT ( 'FLAGSET_FLAGS6' )
ENUM_ELEMENT ( 'FLAGSET_FLAGSST' )
END_ENUM ( 'FLAGSET' )


BEGIN_ENUM ( 'GAMEMODE' )
ENUM_ELEMENT ( 'GAMEMODE_COOPERATIVE' )
ENUM_ELEMENT ( 'GAMEMODE_SURVIVAL' )
ENUM_ELEMENT ( 'GAMEMODE_INVASION' )
ENUM_ELEMENT ( 'GAMEMODE_DEATHMATCH' )
ENUM_ELEMENT ( 'GAMEMODE_TEAMPLAY' )
ENUM_ELEMENT ( 'GAMEMODE_DUEL' )
ENUM_ELEMENT ( 'GAMEMODE_TERMINATOR' )
ENUM_ELEMENT ( 'GAMEMODE_LASTMANSTANDING' )
ENUM_ELEMENT ( 'GAMEMODE_TEAMLMS' )
ENUM_ELEMENT ( 'GAMEMODE_POSSESSION' )
ENUM_ELEMENT ( 'GAMEMODE_TEAMPOSSESSION' )
ENUM_ELEMENT ( 'GAMEMODE_TEAMGAME' )
ENUM_ELEMENT ( 'GAMEMODE_CTF' )
ENUM_ELEMENT ( 'GAMEMODE_ONEFLAGCTF' )
ENUM_ELEMENT ( 'GAMEMODE_SKULLTAG' )
ENUM_ELEMENT ( 'GAMEMODE_DOMINATION' )
END_ENUM ( 'GAMEMODE' )

