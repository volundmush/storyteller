LOOP = """@assert hasflag(%#,CONNECTED);th setq(who,setunion(lwho(),,%b,namei));@pemit me=u(BOT_INCOMING,CLEAR,Yes);@wait 1=@pemit me=u(BOT_INCOMING,LWHO,%q<who>);@wait 3=th step(STEPFORMAT,%q<who>,30);@wait 30=@trigger me/LOOP"""

STARTUP = "@trigger me/LOOP"

INCOMING = "^^^%0: %1"

PAGEFORMAT = "$$$%# %0"

CHATFORMAT = """[if(strmatch(%#,%!),,***[stripansi(%1)]: %#~~~%4~~~%2)]"""

WHOHEAD = """[align(23 10 9 5 5,Name,Alias,Sex,Conn,Idle)]"""
WHOLINE = """[align(23 10 9 5 5,%0,%1,%2,%3,%4)]"""

STEPFORMAT = """[pemit(me,u(BOT_INCOMING,WHODATA,[iter(iter(lnum(%+),r(%i0,args)),%i0~[name(%i0)]~[alias(%i0)]~[default(%i0/SEX,?)]~[etime(conn(%i0),3)]~[etime(idle(%i0),3)],%b,^)]))]"""

ALL_LINES = {'BOT_INCOMING': INCOMING, 'PAGEFORMAT': PAGEFORMAT, 'CHATFORMAT': CHATFORMAT, 'LOOP': LOOP,
             'BOT_WHOLINE': WHOLINE, 'BOT_WHOHEAD': WHOHEAD, 'STARTUP': STARTUP, 'STEPFORMAT': STEPFORMAT}