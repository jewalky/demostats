# -*- coding: utf-8 -*-

import sys
import inspect

#####################################################
## AUXILIARY FUNCTIONS TO MAKE ENUM PORTING EASIER ##
#####################################################



TOP_ENUMS = {}
CURRENT_ENUM = None

class EnumError(Exception):
    pass

def AUX_GET_MODULE():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    return mod
    
def AUX_SETUP_ENUMS(mod):
    if not hasattr(mod, '__TOP_ENUMS__') or not hasattr(mod, '__CURRENT_ENUM__'):
        setattr(mod, '__TOP_ENUMS__', {})
        setattr(mod, '__CURRENT_ENUM__', None)
        
def BEGIN_ENUM(name):
    mod = AUX_GET_MODULE()
    AUX_SETUP_ENUMS(mod)
    mod.__TOP_ENUMS__[name] = 0
    mod.__CURRENT_ENUM__ = name
    
def END_ENUM(name):
    mod = AUX_GET_MODULE()
    del mod.__TOP_ENUMS__[name]
    mod.__CURRENT_ENUM__ = None
    
def ENUM_ELEMENT2(name, value):
    mod = AUX_GET_MODULE()
    if mod.__CURRENT_ENUM__ is None:
        raise EnumError('Current enum is null')
    if type(value) != int:
        raise EnumError('Enum value should be int')
    mod.__TOP_ENUMS__[mod.__CURRENT_ENUM__] = value+1
    setattr(mod, name, value)
    
def ENUM_ELEMENT(name):
    mod = AUX_GET_MODULE()
    if mod.__CURRENT_ENUM__ is None:
        raise EnumError('Current enum is null')
    setattr(mod, name, mod.__TOP_ENUMS__[mod.__CURRENT_ENUM__])
    mod.__TOP_ENUMS__[mod.__CURRENT_ENUM__] += 1

def to_string(where, value, allowed_beginning):
    variables = vars(where)
    for k in variables:
        v = variables[k]
        allowed = False
        for ab in allowed_beginning:
            if k[:len(ab)].lower() == ab.lower():
                allowed = True
                break
        if allowed and v == value:
            return k
    return '<null>'