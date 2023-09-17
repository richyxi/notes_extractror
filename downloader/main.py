# importing packages
from pytube import YouTube
import os
import json
from pydub import AudioSegment
import datetime


def cutter(file, out,start, end):
    sm, ss = start
    em, es = end

    start = datetime.time(0, sm, ss) 
    s = int(datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second).total_seconds()) * 1000

    end = datetime.time(0, em, es) 
    e = int(datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second).total_seconds()) * 1000

    newAudio = AudioSegment.from_file(file)
    newAudio = newAudio[s:e]
    newAudio.export(out + '/song.mp3', format="mp3")

# url input from user
def download(link, start=None, end=None, segment_name=None):
    yt = YouTube(link)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    #song data
    metadata = {
        "title": yt.title,
        "has_split": False,
        "segment_name": None
    }

    # check for destination to save file
    destination = "sink/in"
    
    # download the file
    out_file = video.download(output_path=destination)
    
    if start:
        new_file = destination + "/pre_song.mp3"
        os.rename(out_file, new_file)
        cutter(new_file, destination, start, end)

        metadata["has_split"] = True
        metadata["segment_name"] = segment_name


    else:
        new_file = destination + "/song.mp3"
        os.rename(out_file, new_file)

    

    # Serializing json
    json_object = json.dumps(metadata, indent=4)
    
    # Writing to sample.json
    with open("sink/in/metadata.json", "w") as outfile:
        outfile.write(json_object)

    # result of success
    print(yt.title + " has been successfully downloaded.")



