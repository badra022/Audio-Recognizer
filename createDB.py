import sqlite3
import os
from pydub import AudioSegment
from tempfile import mktemp
import numpy as np
import os
import pylab
import librosa
import librosa.display
import sklearn
import matplotlib.pyplot as plt
from PIL import Image
import imagehash
from classes import SongRecord


conn = sqlite3.connect('../shazam_demo/database.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Songs')

cur.executescript('''
CREATE TABLE Songs (
    id INTEGER NOT NULL, 
    hash_spectrogram TEXT, 
    hash_centroid_feature TEXT, 
    hash_rolloff_feature TEXT ,
    hash_chroma_feature TEXT ,
    name TEXT NOT NULL PRIMARY KEY UNIQUE
    );''')



id = 1
directory = r'D:\active-gits\shazam_demo/spectrograms' # directory for the shared spectrogram files folder
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        print(filename)
        if filename:
            song = SongRecord(songName = filename)
        else:
            print("Song Spectrogram Not found!")

        song.insertToDatabase()