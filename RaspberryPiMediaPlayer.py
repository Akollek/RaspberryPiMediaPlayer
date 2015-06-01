from Cocoa import *
from Foundation import NSObject
from PyObjCTools import AppHelper
from scp_handler import SCPHandler
from omxplayer import OMXPlayer
from threading import Thread
import os, re, time


def string_to_path(string):
    rstring = string
    chars_to_escape = (' ', '(', ')', '[', ']', ':')
    for c in chars_to_escape:
        rstring = rstring.replace(c, '\\'+c)
    return rstring


class RPiMediaPlayerController(NSWindowController):

    audio_formats = ['mp3','mpa','flac','ogg','wav','wma','m4a']
    video_formats = ['avi','wmv','mpg','mpeg','mp4','mkv','m4v','m2v','mpv','ogv','flv','mov'] 
    media_patterns = re.compile(".*\.("+"|".join(audio_formats+video_formats)+")$", re.IGNORECASE)

    hostnameField = objc.IBOutlet()
    usernameField = objc.IBOutlet()
    passwordField = objc.IBOutlet()
    filenameField = objc.IBOutlet()
    messageField  = objc.IBOutlet()
    nowPlayingField = objc.IBOutlet()

    playButton = objc.IBOutlet()
    fButton    = objc.IBOutlet()
    ffButton   = objc.IBOutlet()
    bButton    = objc.IBOutlet()
    bbButton   = objc.IBOutlet()
    stopButton = objc.IBOutlet()
    volupButton   = objc.IBOutlet()
    voldownButton = objc.IBOutlet()
    
    uploadButton = objc.IBOutlet()

    playButtons = (
            'playButton',
            'fButton',
            'ffButton',
            'bButton',
            'bbButton',
            'stopButton',
            'volupButton',
            'voldownButton',
            )
    
    def setPlayButtons(self,enable):
        for button in self.playButtons:
            eval('self.{}'.format(button)).setEnabled_(enable)

    def scp_and_play(self):
        self.scp_handler = SCPHandler(self.hostname,self.username,self.password)
        self.remote_file = "/tmp/{}".format(self.filename.split("/")[-1])
        self.scp_handler.scp(self.filename,self.remote_file)
        filename = self.filename.split("/")[-1].replace("\\","")
        self.messageField.setStringValue_("Upload starting...")
        time.sleep(0.5)
        while self.scp_handler.progress != 100:
            time.sleep(0.1)
            message = "Uploading {filename} to {remote}\nProgress: {p}%".format(
                                filename=filename,
                                remote=self.hostname,
                                p=self.scp_handler.progress)
            self.messageField.setStringValue_(message)
        
        message = "Uploading {filename} to {remote}\nProgress: Done".format(
                                filename=filename,
                                remote=self.hostname)
        self.messageField.setStringValue_(message)
        
        # start player
        self.omxplayer = OMXPlayer(self.hostname, self.username, self.password)
        self.omxplayer.play(self.remote_file)
        self.nowPlayingField.setStringValue_("Currently Playing:\n{}".format(filename))
        self.setPlayButtons(True)

        # poll for status of video
        # (don't start polling until omxplayer has had some time to get started)
        time.sleep(10)
        while self.omxplayer.playing:
            time.sleep(1)

        # reset when playing is done
        self.setPlayButtons(False)
        self.uploadButton.setEnabled_(True)
        self.nowPlayingField.setStringValue_("Nothing playing")

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.setPlayButtons(False)

    @objc.IBAction
    def upload_(self, sender):
        self.hostname = self.hostnameField.stringValue()
        self.username = self.usernameField.stringValue()
        self.password = self.passwordField.stringValue()
        self.filename = self.filenameField.stringValue()
        if not os.path.isfile(self.filename):
            self.messageField.setStringValue_("File not found.")
            return
        if not self.media_patterns.match(self.filename):
            self.messageField.setStringValue_("Please only provide audio or video files")
            return
        self.uploadButton.setEnabled_(False)
        self.filename = string_to_path(self.filename)
        scp_and_play_thread = Thread(target=self.scp_and_play, args=())
        scp_and_play_thread.daemon = True
        scp_and_play_thread.start()
    
    @objc.IBAction
    def playpause_(self, sender):
        self.omxplayer.toggle_play()

    @objc.IBAction
    def f_(self, sender):
        self.omxplayer.f()

    @objc.IBAction
    def ff_(self, sender):
        self.omxplayer.ff()

    @objc.IBAction
    def b_(self, sender):
        self.omxplayer.b()

    @objc.IBAction
    def bb_(self, sender):
        self.omxplayer.bb()

    @objc.IBAction
    def volup_(self, sender):
        self.omxplayer.volup()

    @objc.IBAction
    def voldown_(self, sender):
        self.omxplayer.voldown()

    @objc.IBAction
    def stop_(self, sender):
        self.omxplayer.close()
        self.setPlayButtons(False)
        self.uploadButton.setEnabled_(True)
        self.nowPlayingField.setStringValue_("Nothing playing")


if __name__=="__main__":
    app = NSApplication.sharedApplication()

    playerController = RPiMediaPlayerController.alloc().initWithWindowNibName_("RaspberryPiMediaPlayer") 
    playerController.showWindow_(playerController)

    NSApp.activateIgnoringOtherApps_(True)
    AppHelper.runEventLoop()

