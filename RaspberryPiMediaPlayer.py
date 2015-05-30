from Cocoa import *
from Foundation import NSObject
from PyObjCTools import AppHelper
from omxplayer import OMXPlayer
import auth_info

class RPiMediaController(NSWindowController):

    fileNameField = objc.IBOutlet()

    def initiliaze(self, filename, hostname, username, password):
        self.omxplayer = OMXPlayer(hostname, username, password)
        self.filename = filename

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.omxplayer = OMXPlayer(auth_info.hostname, auth_info.username)
        # temporary hard coding until I look into choosing a file
        self.omxplayer.play('/home/pi/Video/Adventure\ Time\ -\ 413a\ -\ I\ Remember\ You\ \(PotentPotables\).mp4')
        filename =self.omxplayer.filename.split("/")[-1].replace("\\","")
        self.fileNameField.setStringValue_("Currently Playing:\n{}".format(filename))
        print(self.fileNameField.stringValue())

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


if __name__=="__main__":
    app = NSApplication.sharedApplication()

    playerController = RPiMediaController.alloc().initWithWindowNibName_("RaspberryPiMediaPlayer")
    
    playerController.showWindow_(playerController)

    NSApp.activateIgnoringOtherApps_(True)
    AppHelper.runEventLoop()

