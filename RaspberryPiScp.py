from Cocoa import *
from Foundation import NSObject
from PyObjCTools import AppHelper
from scp_handler import SCPHandler
from threading import Thread
import os, time

class RPiScpController(NSWindowController):
    hostnameField = objc.IBOutlet()
    usernameField = objc.IBOutlet()
    passwordField = objc.IBOutlet()
    filenameField = objc.IBOutlet()
    messageField  = objc.IBOutlet()
    progressField = objc.IBOutlet()
    watchButton   = objc.IBOutlet()

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.watchButton.setEnabled_(False)


    @objc.IBAction
    def upload_(self, sender):
        self.hostname = self.hostnameField.stringValue()
        self.username = self.usernameField.stringValue()
        self.password = self.passwordField.stringValue()
        self.filename = self.filenameField.stringValue()
        if not os.path.isfile(self.filename):
            self.messageField.setStringValue_("File not found.")
            return
        self.scp_handler = SCPHandler(self.hostname,self.username,self.password)
        self.remote_file = "/tmp/{}".format(self.filename.split("/")[-1])
        self.scp_handler.scp(self.filename,self.remote_file)
        while self.scp_handler.progress != 100:
            time.sleep(0.5)
            message = "Uploading {filename} to {rfile}...\nProgress: {p}%".format(
                                filename=self.filename,
                                rfile=self.remote_file,
                                p=self.scp_handler.progress)
            self.messageField.setStringValue_(message)
        self.watchButton.setEnabled_(True)


if __name__=="__main__":
    app = NSApplication.sharedApplication()

    scpController = RPiScpController.alloc().initWithWindowNibName_("RaspberryPiMediaScp")
    
    scpController.showWindow_(scpController)

    NSApp.activateIgnoringOtherApps_(True)
    AppHelper.runEventLoop()

