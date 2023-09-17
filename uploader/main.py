from pyicloud import PyiCloudService
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import sys
import json

metadata = "sink/in/metadata.json"
midi_path = "sink/out/midi"
song_path = "sink/out/song"


# Python program to read
# json file



###########
song_files = [
    "bass.wav",
    "drums.wav",
    "other.wav",
    "piano.wav",
    "vocals.wav"
]

midi_files = [
    "bass_basic_pitch.mid",
    "drums_basic_pitch.mid",
    "other_basic_pitch.mid",
    "piano_basic_pitch.mid",
    "vocals_basic_pitch.mid",
]


def to_icloud():
    api = PyiCloudService('*', '')
    # auth
    result = True
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input(
            "Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print(
                "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print(
                "  %s: %s" % (i, device.get('deviceName',
                                            "SMS to %s" % device.get('phoneNumber')))
            )

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)

    print(api.drive.dir())

    # upload info
    api.drive['audio_files'].mkdir(title)
    api.drive['audio_files'][title].mkdir("out")

    api.drive['audio_files'][title]["out"].mkdir("midi")
    api.drive['audio_files'][title]["out"].mkdir("song")

    #

    # song upload
    for song_file in song_files:
        file = song_path + "/" + song_file

        print(file)
        with open(file, 'rb') as file_in:
            api.drive['audio_files'][title]["out"]["song"].upload(file_in)

    # song upload
    for midi_file in midi_files:
        file = midi_path + "/" + midi_file

        with open(file, 'rb') as file_in:
            api.drive['audio_files'][title]["out"]["midi"].upload(file_in)


def to_gd(title_in=None):

    # Opening JSON file
    f = open(metadata)

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    print(data)
    title = data["title"]
    has_split = data["has_split"]
    seg_name = data["segment_name"]


    # Closing file
    f.close()

    gauth = GoogleAuth()
    # client_secrets.json need to be in the same directory as the script
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    print(title)
    #buscar el id del title
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    title_folder_id = None
    for file in fileList:
        if(file['title'] == title):
            title_folder_id = file['id']

    # primero se crean las carpetas
    if title_folder_id is None:
        # no existe la cancion en drive
        file_metadata = {
            'title': title,
            'parents': [{"id":"1diP9MMnV30z3vNTavyfCAAQKwsSvvQHL"}],
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder_title = drive.CreateFile(file_metadata)
        folder_title.Upload()
    
    if has_split:
        file_metadata = {
            'title': seg_name,
            'parents': [{"id":"1diP9MMnV30z3vNTavyfCAAQKwsSvvQHL"}],
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder_title = drive.CreateFile(file_metadata)
        folder_title.Upload()
        title_folder_id = folder_title["id"]


    # crear carpetas midi, songo
    midi_metadata = {
        'title': "midi",
        'parents': [{"id":title_folder_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    song_metadata = {
        'title': "song",
        'parents': [{"id":title_folder_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder_midi = drive.CreateFile(midi_metadata)
    folder_midi.Upload()

    folder_song = drive.CreateFile(song_metadata)
    folder_song.Upload()

    for song_file in song_files:
        file = song_path + "/" + song_file

        song_file_meta = {
            'title': song_file,
            'parents': [{"id":folder_song["id"]}],
        }

        file_song = drive.CreateFile(song_file_meta)

        file_song.SetContentFile(file)
        file_song.Upload()  # Upload the file.

    for midi_file in midi_files:
        file = midi_path + "/" + midi_file

        midi_file_meta = {
            'title': midi_file,
            'parents': [{"id":folder_midi["id"]}],
        }

        file_song = drive.CreateFile(midi_file_meta)

        file_song.SetContentFile(file)
        file_song.Upload()  # Upload the file.


def upload(icloud=None, gd=None, title_in=None):

    if icloud:
        to_icloud()

    if gd:
        to_gd()
