# raspi-radio-box
Raspi-radio-box is an internet radio streaming script using the VLC python library to connect and play the radio streams. The streams are stored remotely in a Google spread sheet to easily update or add streams.

[Place holder for image and video]

For input I have a USB number pad connected via USB to the Raspberry pi 2B+ where I detect the key presses. The available keys are:

- 1 - 9 directly access frequently used for favorite streams.
- Volume up and down
- Pause stream
- Mute stream
- End player 
- [0] key = pick a random stream from the spreadsheet if there are more than 9 streams
- [.] key = Sequentially increment through the streams from the spreadsheet if there are more than 9 streams

There are also three indicator led's.
- Green = player ready
- Yellow = pause and Raspberry pi booting indicator
- Red = mute


### Set up
Install
```sh
python-vlcs
python-vlc
gspread
oauth2client
```


### Resources I used to get things working
https://raspberrypi.stackexchange.com/questions/38794/enable-num-lock-at-boot-raspberry-pi
https://www.raspberrypi-spy.co.uk/2018/11/raspberry-pi-7-segment-led-display-module-using-python/
https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

License
----

MIT
