# Rhapsody2Gmusic

Converts a Rhapsody playlist to a Google Music playlist.  This uses the [Unofficial Google Music API](https://github.com/simon-weber/gmusicapi) and was tested against version 7.0.0-dev. Requires a Google Music All Access account.

## Install

```
git clone https://github.com/judsonmitchell/rhapsody2gmusic
```

Install the dependencies: 
gmusicapi >= 7.0.0-dev
bs4 >= 4.0.2

## Configuration

You can simplify the process by adding an optional .config file with the following syntax (see .config_TEMPLATE):

```
email <your email address>
password <your password - optional>
android_device_id <your android device id - 16 hex digits, eg '1234567890abcdef'>
```
The Android device ID is a 16-digit hexadecimal string (without a
'0x' prefix) identifying an Android device or a string of the form
`ios:01234567-0123-0123-0123-0123456789AB` (including the `ios:`
prefix) identifying an iOS device you must already have registered
for Google Play Music. On Android, you can obtain this ID by dialing
`*#*#8255#*#*` on your phone or using this
[App](https://play.google.com/store/apps/details?id=com.evozi.deviceid)
(see the Google Service Framework ID Key).

## Usage

```
python rhapsody2gmusic.py
```

If you have not created a .config file, you will be prompted for your log in information. You will then be prompted for a Rhapsody playlist URL which should be the url provided by the social sharing options, e.g http://www.rhapsody.com/playlist/mp.145164964

The script will then scrape the track metadata from the playlist page and attempt to match that information against the Gmusic API.  The script will tell you how many tracks have been successfully matched and then create a playlist of the same name on Google Music.

## License

MIT
