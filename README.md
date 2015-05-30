Raspberry Pi Python Media Player
================================

A python backed giu to play movies on your computer over a raspberry pi hooked up to a TV


### Use:
    Store ip and username of raspberry pi hooked up into a TV over HDMI in `auth_info.py` in root directory (assumes assumes public key auth is set up).
    Create an aliased version of the app with  `python setup.py py2app -A`.
    Run the app with `dist/RaspberryPiMediaPlayer.app/Contents/MacOS/RaspberryPiMediaPlayer`.


### TODO:
- Get volume controls working
- Let users choose and scp a file over 
- Error handling (cannot connect to the raspberry pi, file does not exist...)

