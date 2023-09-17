from basic_pitch.inference import predict_and_save


def convert_to_midi():

    path_to = "sink/out/song/" 
    output = "sink/out/midi"


    
    files = [
        path_to + "bass.wav", 
        path_to + "drums.wav", 
        path_to + "other.wav", 
        path_to + "piano.wav", 
        path_to + "vocals.wav"]


    predict_and_save(
        files,
        output,
        True,
        False,
        False,
        False,
    )

    print("looks like it finished")