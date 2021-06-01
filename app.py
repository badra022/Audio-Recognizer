###########################################################
# authors: Ahmed Badra,
#          Hassan Hosni,
#          Yousof Elhely,
#          Moamen Gamal
#
# title: Biosignal viewer
#
# file: main program file (RUN THIS FILE)
############################################################

# libraries needed for main python file
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
import sys
from gui import Ui_MainWindow
import os
from classes import Song, SongRecord
import pathlib
from helpers import getWeightedAverageWav, getSimilarityIndex, Sort_Tuple, convertToInvertedPercentage
import numpy as np

# class definition for application window components like the ui
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.song1Path = None
        self.song2Path = None
        self.ui.open1.clicked.connect(lambda: self.open(1))
        self.ui.open2.clicked.connect(lambda: self.open(2))
        self.ui.slider.sliderReleased.connect(self.recognize)

    def open(self, song_number):
        # print("opening choosing window.....")
        files_name = QFileDialog.getOpenFileName( self, 'Open only mp3', os.getenv('HOME') ,"mp3(*.mp3)")
        path = files_name[0]
        # print("opening choosing window.....")

        if pathlib.Path(path).suffix == ".mp3":
            if song_number == 1:
                if self.song1Path is not None:
                    print("already selected song1")
                else:
                    self.song1Path = path
            if song_number == 2:
                if self.song2Path is not None:
                    print("already selected song2")
                else:
                    self.song2Path = path

        if self.song1Path is not None and self.song2Path is not None:
            self.recognize()

    def recognize(self):
        data, fs = getWeightedAverageWav(self.song1Path, self.song2Path, self.ui.slider.value())
        song = Song(wavdata = data, samplingFrequency = fs)
        InputFeatures = np.array([song.getFeature_centroid(), song.getFeature_chroma(), song.getFeature_rolloff()])
        results = []
        
        # print(song.getHashedSpectrogram())
        # print(song.getFeature_centroid())
        # print(song.getFeature_chroma())
        # print(song.getFeature_rolloff())
        # print(SongRecord.getAllSongs())
        records = SongRecord.getAllSongs()
        for record in records:
            results.append((record[5], getSimilarityIndex(InputFeatures, record))) # store record name and it's similarity index
            # print((record[5],"    ->    ", getSimilarityIndex(song, record)))
        results = Sort_Tuple(results)
        results = convertToInvertedPercentage(results)
        # print(results)
        row = 0
        for result in results:
            self.ui.resultTable.setItem(row, 0, QTableWidgetItem(str(result[0])))
            self.ui.resultTable.setItem(row, 1, QTableWidgetItem(str(result[1])))
            row = row + 1


# function for launching a QApplication and running the ui and main window
def window():
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()