import re
import pexpect
from threading import Thread

def update_progress(locals):
    self = locals['extra_args']['self']
    child = locals['child']
    self.progress=int(
            re.search(r'\b(\d+)(%)' , child.after).group(1)
            )

class SCPHandler(object):
    """
    Class to handle scp operations (local -> remote) 
    """

    def __init__(self, host, user, password=""):
        self.host = host
        self.user = user
        # password only required if public key auth not set up
        self.password = password

    def scp(self, f, remote_dir):
        scp_thread = Thread(target=self.scp_daemon, args=(f,remote_dir))
        scp_thread.daemon = True
        scp_thread.start()

    def scp_daemon(self, f, remote_dir):
        self.progress = 0
        command = 'scp {f} {user}@{host}:{remote_dir}'.format(
                        f = f,
                        user = self.user,
                        host = self.host,
                        remote_dir = remote_dir)
        pexpect.run(command,
                    events={
                        '[Pp]assword:':self.password,
                        r'\d+%':update_progress
                    },
                    extra_args={
                        'self':self
                    })
    
