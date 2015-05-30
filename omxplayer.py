import pxssh
import time
from threading import Thread

class OMXPlayer(object):
    """
    Class to handle the ssh session used to control omxplayer
    """
    UP    = '\x1b[A'
    DOWN  = '\x1b[B'
    RIGHT = '\x1b[C'
    LEFT  = '\x1b[D'


    def __init__(self,hostname,username,password=""):
        self.session = pxssh.pxssh()
        self.session.login(hostname,username,password)
        self.playing = False
    
    def play(self, filename):
        self.filename = filename
        self.volume = 0
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
        self.session.sendline(OMXPlayer.RIGHT)

    def ff(self): # seek forward faster
        self.session.sendline(OMXPlayer.UP)

    def b(self): #seek backwards
        self.session.sendline(OMXPlayer.RIGHT)

    def bb(seld):
        self.session.sendline(OMXPlayer.DOWN)

    def volup(self):
        self.session.sendline("+")
        self.volume += 3 # omxplayer works in units of three dBs

    def voldown(self):
        self.session.sendline("-")
        self.volume -= 3

    def close(self):
        self.session.sendline('\003') # send control-C
        time.sleep(2) # give omxplayer time to close
        self.session.sendline('rm {}'.format(self.filename))
        self.session.logout()

