# This is it. The key library after going through so many different libraries/sources.
# pyaudio, pulseaudio, sounddevice, aslaaudio, pulsectl
import soundcard as sc
import soundfile as sf
from modules.analyzer import Analyzer
import numpy as np
import matplotlib.pyplot as plt
from modules.waveform_plot import WaveformPlot
from modules.librosa_chroma import LibrosaChroma
from modules.visualizer import Visualizer
import pandas as pd
from PySide2 import QtCore, QtWidgets
# from modules.analysis import AnalysisPlot

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 15                  # [sec]. duration recording audio.

LENGTH = SAMPLE_RATE*RECORD_SEC
AMP_CONSTANT = 6000

print(f'Default Speaker: \n\t{sc.default_speaker()}')

wplot = WaveformPlot(SAMPLE_RATE, LENGTH, AMP_CONSTANT)
wplot.setup_fig()
mood_table = [
    "happy", 
    "sad", 
    "aggressive", 
    "chill",  
    "energetic",
]
color_table = [
    [15, 252, 3],
    [15, 3, 252],
    [252, 15, 3],
    [252, 3, 252],
    [252, 252, 3]
]
training_labels = [i for i in [2, 4, 0, 3, 1] for j in range(15)]
data = pd.read_csv("./data.csv")
print("Grabbing training data.")
data = data.iloc[:len(training_labels)]
print(data)
data["training_labels"] = training_labels
print("Initializing data...")
analyzer = Analyzer(mood_table=mood_table, data=data, color_table=color_table,output_path="./data",num_cols=48)
libchroma = LibrosaChroma(SAMPLE_RATE)
with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
    
    # data = mic.record(numframes=None)
    # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
    # while True:
    print("Recording data...")
    data_output = speaker.record(numframes=LENGTH)
    
    # Normalize the array by an integer, Resize it to fit the graph
    data_output_normal = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
    data_output_normal  = np.resize(data_output_normal, LENGTH)
    
    wplot.draw(data_output_normal)
    data_output = np.ndarray.flatten(data_output)
    print(data_output, '\n', len(data_output))
    
    features = analyzer.analyze(raw_data=data_output)
    prediction = analyzer.predict(features = features, nearest_neighbor = 2, pca_dim = 3)
    
    visualizer = Visualizer()

    visualizer.show(color = prediction["color"]["hex"])
    #libchroma.create_chroma(data_output)
    #libchroma.plot_chroma()
    
    
    

        
    # sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    
