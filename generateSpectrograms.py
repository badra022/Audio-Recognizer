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

# Normalising the spectrals for visualisation
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)

directory = r'D:\active-gits\songs_drive' # directory for the shared mp3 files folder
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        print(filename)
        sound = AudioSegment.from_file(filename, format="mp3")[:60000]  # read mp3
        wavfile = mktemp('.wav')  # use temporary file
        sound.export(wavfile, format="wav")  # convert to wav
        wavdata,samplingFrequency =librosa.load(wavfile, sr = None)

        Spectro_Path = 'D:/active-gits/shazam_demo/spectrograms/' + os.path.splitext(os.path.basename(filename))[0]+'.png'
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        S = librosa.amplitude_to_db(np.abs(librosa.stft(wavdata)), ref=np.max)
        librosa.display.specshow(S, y_axis='linear')
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()

        S = np.abs(librosa.stft(wavdata))

        centroid_Path = 'D:/active-gits/shazam_demo/centroid_feature/' + os.path.splitext(os.path.basename(filename))[0]+'.png'
        #spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_centroids = librosa.feature.spectral_centroid(S = S, sr = samplingFrequency)
        librosa.display.specshow(spectral_centroids)
        pylab.savefig(centroid_Path, bbox_inches=None, pad_inches=0)
        pylab.close()

        rolloff_Path = 'D:/active-gits/shazam_demo/rolloff_feature/' + os.path.splitext(os.path.basename(filename))[0]+'.png'
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_rolloffs = librosa.feature.spectral_rolloff(S = S, sr = samplingFrequency)
        librosa.display.specshow(spectral_rolloffs)
        pylab.savefig(rolloff_Path, bbox_inches=None, pad_inches=0)
        pylab.close()

        chroma_Path = 'D:/active-gits/shazam_demo/chroma_feature/' + os.path.splitext(os.path.basename(filename))[0]+'.png'
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_chroma = librosa.feature.chroma_stft(S = S, sr = samplingFrequency)
        librosa.display.specshow(spectral_chroma)
        pylab.savefig(chroma_Path, bbox_inches=None, pad_inches=0)
        pylab.close()
    else:
        continue
