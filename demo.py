# -*- coding: utf-8 -*-

from stream import *
from data import *

import sys
import os


def CLIENTDEMO_Read(fn, callback):
    stream = open(fn, 'rb')

    # read demo header, assume its always the same

    class DemoError(Exception):
        pass

    if stream.read(4) != b'ZCLD':
        raise DemoError('Expected ZCLD demo')
        
    #if NETWORK_ReadUByte(stream) != CLD_DEMOLENGTH:
    #    raise DemoError('Invalid demo header: expected CLD_DEMOLENGTH')

    # we can't do Zandronum behavior here.
    # CLD_DEMOLENGTH is assumed to be legit, and off it values for other CLD_ enums are calculated.
    # this is required to support multiple demo versions.
    CLD_DEMOLENGTH = NETWORK_ReadUByte(stream)
    CLD_DEMOVERSION = CLD_DEMOLENGTH+1
    CLD_CVARS = CLD_DEMOLENGTH+2
    CLD_USERINFO = CLD_DEMOLENGTH+3
    CLD_BODYSTART = CLD_DEMOLENGTH+4
    CLD_TICCMD = CLD_DEMOLENGTH+5
    CLD_LOCALCOMMAND = CLD_DEMOLENGTH+6
    CLD_DEMOEND = CLD_DEMOLENGTH+7
    CLD_DEMOWADS = CLD_DEMOLENGTH+8
        
    g_lDemoLength = NETWORK_ReadULong(stream)

    DOTVERSIONSTR = None
    bBodyStart = False
    while not bBodyStart:
        lCommand = NETWORK_ReadUByte(stream)
        
        if lCommand == CLD_DEMOVERSION:
            lDemoVersion = NETWORK_ReadShort(stream)
            DOTVERSIONSTR = NETWORK_ReadString(stream)
            print('Version %s demo' % DOTVERSIONSTR)
            BUILD_ID = NETWORK_ReadUByte(stream)
            rngseed = NETWORK_ReadULong(stream)
            break

    if DOTVERSIONSTR is None:
        raise DemoError('No version found in the demo')

    # now use DOTVERSIONSTR to determine further parser
    # a parser is basically python module which receives stream and callback.
    
    basever = DOTVERSIONSTR.split('-')[0]
    # for example, 2.1.2
    # query modules
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/versions')
    modules = os.listdir('versions')
    
    mod_parse = None
    mod_parse_header = None
    for module in modules:
        module = module.lower()
        # if it doesn't end with .py, we don't need it
        if module[-3:] != '.py':
            continue
        module = module[:-3]
        if module == '__init__':
            continue
        # try importing this
        try:
            mod = __import__('versions.'+module, globals(), locals(), ['version', 'next_header', 'next_packet'], 0)
        except ImportError:
            continue
        if not hasattr(mod, 'version') or not hasattr(mod, 'next_header') or not hasattr(mod, 'next_packet'):
            continue
        # module class should have function called version() which specifies applicable versions (list)
        if basever in mod.version():
            mod_parse = mod.next_packet
            mod_parse_header = mod.next_header
            break

    if mod_parse is None:
        raise DemoError('No suitable parser found for version %s (%s)' % (basever, DOTVERSIONSTR))
        
    while not bBodyStart:
        lCommand = NETWORK_ReadUByte(stream)
        
        if lCommand == CLD_BODYSTART:
            bBodyStart = True
            
        else:
            stream.seek(stream.tell()-1)
            pkt = mod_parse_header(stream)
            if pkt is None:
                raise DemoError('Unknown demo header %02X (%d)' % (lCommand, lCommand))
            # run callback on packet?..
            # yup
            callback(Struct(**pkt))
        
    while True:
        try:
            lCommand = NETWORK_ReadUByte(stream)
            if lCommand == 255:
                raise
        except:
            print('Demo ended.')
            break
        stream.seek(stream.tell()-1)
        pkt = mod_parse(stream)
        if pkt is None:
            raise DemoError('Unknown demo packet %02X (%d)' % (lCommand, lCommand))
        # run callback on packet
        callback(Struct(**pkt))
        if pkt['name'] == 'CLD_DEMOEND':
            print('Demo ended.')
            break

