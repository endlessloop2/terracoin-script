#! /usr/bin/env python
from subprocess import Popen,PIPE,STDOUT
import collections
import os
import sys
import time
import math
import os
import time
from urllib2 import urlopen

BOOTSTRAP_URL = "https://mega.nz/#!8qZ0EZ4L!3opQ7VlNkcTC_syuLLTHUTdYmjZKJ1cnTxcWVZZkX8Y" #TODO
SENTINEL_GIT_URL = "https://github.com/terracoin/sentinel.git"

MN_USERNAME = ""
MN_PORT = 13333
MN_RPCPORT = 22350
MN_NODELIST = ""

MN_LFOLDER = ".terracoincore"
MN_WFOLDER = "TerracoinCore"
MN_CONFIGFILE = "terracoin.conf"
MN_DAEMON = "terracoind"
MN_CLI = "terracoin-cli"
MN_EXPLORER = "https://explorer.terracoin.io/"
MASTERNODES = ""

SERVER_IP = urlopen('http://ip.42.pl/raw').read()
DEFAULT_COLOR = "\x1b[0m"
PRIVATE_KEY = ""

def print_info(message):
    BLUE = '\033[94m'
    print(BLUE + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_warning(message):
    YELLOW = '\033[93m'
    print(YELLOW + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_error(message):
    RED = '\033[91m'
    print(RED + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def get_terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
    
def remove_lines(lines):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for l in lines:
        sys.stdout.write(CURSOR_UP_ONE + '\r' + ERASE_LINE)
        sys.stdout.flush()

def run_command_as(user, command):
    run_command('su - {} -c "{}" '.format(user, command))

def run_command(command):
    out = Popen(command, stderr=STDOUT, stdout=PIPE, shell=True)
    lines = []
    
    while True:
        line = out.stdout.readline()
        if (line == ""):
            break
        
        # remove previous lines     
        remove_lines(lines)
        
        w, h = get_terminal_size()
        lines.append(line.strip().encode('string_escape')[:w-3] + "\n")
        if(len(lines) >= 9):
            del lines[0]

        # print lines again
        for l in lines:
            sys.stdout.write('\r')
            sys.stdout.write(l)
        sys.stdout.flush()

    remove_lines(lines) 
    out.wait()
def awk(command):
    out = Popen(command, stderr=STDOUT, stdout=PIPE, shell=True)
    lines = []
    
    while True:
        line = out.stdout.readline()
        if (line == ""):
            break      
        #lines.append(line.strip().encode('string_escape')[:w-3] + "\n")
        #for l in lines:

    out.wait()
    return lines

def print_welcome():
    os.system('clear')
    GREEN = '\033[32m'
    print(GREEN + "Universal Masternode Updater" + DEFAULT_COLOR)

def check_root():
    print_info("Check root privileges")
    user = os.getuid()
    if user != 0:
        print_error("This program requires root privileges.  Run as root user.")
        sys.exit(-1)

def get_masternodes():
  print_info("Searching for masternode installations..")
  global MASTERNODES
  MASTERNODES = awk("ps auxwww | grep terracoind | grep -v grep | grep -v testnet | awk {'print $1'}")
  for m in MASTERNODES:
    print_info("Masternode found" + m)
    restart_masternode(m)
    

def update_wallet():
    run_command("wget https://masternodes.host/binaries/terracoind -O /usr/local/bin/{}".format(MN_DAEMON))
    run_command("chmod +x /usr/local/bin/{}".format(MN_DAEMON))
    run_command("wget https://masternodes.host/binaries/terracoin-cli -O /usr/local/bin/{}".format(MN_CLI))
    run_command("chmod +x /usr/local/bin/{}".format(MN_CLI))

def restart_masternode(mn_user):
    print_info("Updating masternode " + mn_user)
    subprocess.check_call('su - {} -c "{}" '.format(mn_user, MN_CLI + ' stop'))
    os.system('su - {} -c "{}" '.format(mn_user, MN_DAEMON + ' -reindex'))
    print_warning("Masternode started reindexing...")
    

def update_sentinel():
    # no sentinel support
    if SENTINEL_GIT_URL == "":
        return
    
    print_warning("Not implemented yet")
def end():
    print_warning("Not implemented yet")

def main():
    print_welcome()
    check_root()
    update_wallet()
    get_masternodes()
    update_sentinel()
    end()

if __name__ == "__main__":
    main()
