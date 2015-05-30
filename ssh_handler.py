import pxssh
import time
from threading import Thread

class SSHHandler(object):
    """
    Class to handle the ssh session used to control omxplayer
    """
    KEY_UP = '\x1b[A'
    KEY_DOWN = '\x1b[B'
    KEY_RIGHT = '\x1b[C'
    KEY_LEFT = '\x1b[D'


    def __init__(self,hostname,username,password=""):
        self.session = pxssh.pxssh()
        self.session.login(hostname,username,password)
        self.playing = False
    
    def play(self, filename):
        self.filename = filename
        player_thread = Thread(target=self.player_daemon, args=())
        player_thread.daemon = True
        player_thread.start()
        
    def player_daemon(self):
        command = "omxplayer -o hdmi {}".format(self.filename)
        self.session.sendline(command)
        self.playing = True
        self.session.prompt()
        self.playing = False

    def toggle_play(self):
        self.session.sendline(" ")

    def f(self): # seek forward
        self.session.sendline(SSHHandler.KEY_RIGHT)

    def ff(self): # seek forward faster
        self.session.sendline(SSHHandler.KEY_UP)

    def b(self): #seek backwards
        self.session.sendline(SSHHandler.KEY_RIGHT)

    def bb(self):
        self.session.sendline(SSHHandler.KEY_DOWN)

    def close(self):
        self.session.sendline('\003') # send control-C
        time.sleep(2) # omxplayer time to close
        self.session.logout()
