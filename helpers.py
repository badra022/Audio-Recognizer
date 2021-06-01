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
from operator import itemgetter
from math import *


def getWavFromMp3(mp3filePath):
        sound = AudioSegment.from_file(mp3filePath, format="mp3")[:44100]  # read mp3
        wavfile = mktemp('.wav')  # use temporary file
        sound.export(wavfile, format="wav")  # convert to wav
        wavdata, samplingFrequency =librosa.load(wavfile, sr = None)
        return wavdata, samplingFrequency

def getWeightedAverageWav(filePath1, filePath2, percentage):
    # print(filePath1)
    # print(filePath2)
    # print("percentage is {}".format(percentage))
    data1, samplingFrequency1 = getWavFromMp3(filePath1)
    data2, samplingFrequency2 = getWavFromMp3(filePath2)
    # print("sampling frequency of the first song is {}".format(samplingFrequency1))
    # print("sampling frequency of the second song is {}".format(samplingFrequency2))
    if samplingFrequency1 == samplingFrequency2:
        percentage /= 100
        return (data1 * percentage + data2 * (1 - percentage)), samplingFrequency1
    else:
        print(" the two songs isn't sampled in the same frequency, Cannot be summed together!")

def euclidean_distance(x,y):
    # return sqrt(sum(pow(x[0] - y[0], 2), sum(pow(x[1] - y[1], 2), pow(x[2] - y[2], 2))))
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

def getSimilarityIndex(InputFeatures, recordTuble):
    recordFeatures = np.array([int(recordTuble[2],16), int(recordTuble[4],16), int(recordTuble[3], 16)])
    return euclidean_distance(InputFeatures, recordFeatures)

def convertToInvertedPercentage(list):
    maximum = max(list,key=itemgetter(1))[1]    #faster solution
    result = []
    for index, tuple in enumerate(list):
        result.append((tuple[0], 100 - (tuple[1]/maximum) * 100))

    return result

# Function to sort hte list by second item of tuple
def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1]) 
    return tup 