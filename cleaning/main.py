import os


midi_files = [
    "bass_basic_pitch.mid",
    "drums_basic_pitch.mid",
    "other_basic_pitch.mid",
    "piano_basic_pitch.mid",
    "vocals_basic_pitch.mid",
]

midi_path = "/sink/out/midi"


def delete():
    for file in midi_files:

        ## If file exists, delete it ##
        myfile = midi_path + "/" + file
        if os.path.isfile(myfile):
            os.remove(myfile)
        else:    ## Show an error ##
            print("Error: %s file not found" % myfile)