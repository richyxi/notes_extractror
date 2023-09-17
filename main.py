from downloader.main import download
from segmentation.main import sep
from converter.main import convert_to_midi
from uploader.main import upload
from cleaning.main import delete

 
#ITS PIPELINE CHAMP
download("https://www.youtube.com/watch?v=irzvPo6f1Gs&ab_channel=JuniorH-Topic", (0, 0), (0,36), "se amerita")
sep()
convert_to_midi()
upload(icloud=False, gd=False)
delete()

