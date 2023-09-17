from spleeter.separator import Separator

# Using embedded configuration.

def sep():
    separator = Separator('spleeter:5stems-16kHz')
    separator.separate_to_file('sink/in/song.mp3', 'sink/out')