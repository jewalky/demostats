# -*- coding: utf-8 -*-

import struct

def NETWORK_ReadByte(stream):
    return struct.unpack('<b', stream.read(1))[0]
    
def NETWORK_ReadUByte(stream):
    return struct.unpack('<B', stream.read(1))[0]

def NETWORK_ReadShort(stream):
    return struct.unpack('<h', stream.read(2))[0]
    
def NETWORK_ReadUShort(stream):
    return struct.unpack('<H', stream.read(2))[0]
    
def NETWORK_ReadLong(stream):
    return struct.unpack('<i', stream.read(4))[0]
    
def NETWORK_ReadULong(stream):
    return struct.unpack('<I', stream.read(4))[0]

def NETWORK_ReadSingle(stream):
    return struct.unpack('<f', stream.read(4))[0]
NETWORK_ReadFloat = NETWORK_ReadSingle
    
def NETWORK_ReadDouble(stream):
    return struct.unpack('<d', stream.read(8))[0]
    
def NETWORK_ReadString(stream):
    ss = b''
    while True:
        cs = stream.read(1)
        if not cs:
            break
        if cs == b'\0':
            break
        ss += cs
    return ss.decode('windows-1252')
