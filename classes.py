import sqlite3
from PIL import Image
import imagehash
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

spectrogramPath = 'spectrograms/'
centroidPath = 'centroid_feature/'
rolloffPath = 'rolloff_feature/'
chromaPath = 'chroma_feature/'

class SongRecord(object):
    conn = sqlite3.connect('../shazam_demo/database.sqlite')
    cur = conn.cursor()
    id = 1

    def __init__(self, songName):
        self.id = self.__class__.id
        self.hash_spectrogram = str(imagehash.phash(Image.open(spectrogramPath + songName)))
        try:
            self.hash_centroid_feature = str(imagehash.phash(Image.open(centroidPath + songName)))
            self.hash_rolloff_feature = str(imagehash.phash(Image.open(rolloffPath + songName)))
            self.hash_chroma_feature = str(imagehash.phash(Image.open(chromaPath + songName)))
        except:
            self.hash_centroid_feature = None
            self.hash_rolloff_feature = None
            self.hash_chroma_feature = None
        self.songName = songName
        self.__class__.id = self.__class__.id + 1

    def insertToDatabase(self):
        self.__class__.cur.execute('''INSERT OR IGNORE INTO Songs (hash_spectrogram, hash_centroid_feature, hash_rolloff_feature, hash_chroma_feature, name, id)
        VALUES ( ?, ?, ?, ?, ?, ?)''', (self.hash_spectrogram,
                                        self.hash_centroid_feature, 
                                        self.hash_rolloff_feature, 
                                        self.hash_chroma_feature, 
                                        self.songName, self.id))
        self.__class__.conn.commit()

    @classmethod
    def getAllSongs(cls):
        cls.cur.execute('''SELECT * FROM Songs''')
        return cls.cur.fetchall()

class Song(object):
    def __init__(self, wavdata, samplingFrequency):
        self.wavdata,self.samplingFrequency = wavdata, samplingFrequency
        self.spectrogram = self.getSpectrogram()

    def getSpectrogram(self):
        return np.abs(librosa.stft(self.wavdata))

    def getHashedSpectrogram(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        librosa.display.specshow(librosa.amplitude_to_db(self.spectrogram, ref=np.max), y_axis='linear')
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_centroid(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_centroids = librosa.feature.spectral_centroid(S = self.spectrogram, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_centroids)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_rolloff(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_rolloffs = librosa.feature.spectral_rolloff(S = self.spectrogram, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_rolloffs)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_chroma(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_chroma = librosa.feature.chroma_stft(S = self.spectrogram, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_chroma)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)