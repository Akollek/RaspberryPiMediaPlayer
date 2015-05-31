Raspberry Pi Python Media Player
================================

A python backed giu to play movies on your computer over a raspberry pi hooked up to a TV. [Video here.](https://drive.google.com/file/d/0B4cfhfxMV9mKUUItVnFPTm9Ta2s/view)


### Use:

Create the app with `python setup.py py2app` (may need to run `pip install -r requirements.txt`).
Find the app at `dist/RaspberryPiMediaPlayer`.


### TODO:
- Error handling (bad hostname, cannot connect to the raspberry pi)
- Check filetypes and only accept video and audio
- Disable upload button while playing media
- Delete file and do a proper close when finished playing
