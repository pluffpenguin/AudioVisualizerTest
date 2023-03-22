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
# from PySide2 import QtCore, QtWidgets
# from modules.analysis import AnalysisPlot

class AudioAnalyzerModel:
    def __init__(self, sample_rate = 44100, amp_constant = 6000):
        self.SAMPLE_RATE = sample_rate
        self.AMP_CONSTANT = amp_constant 

    def start(self, 
              mood_table, 
              training_data, 
              training_labels, 
              recording_length = 20, 
              plot_waveform = False, 
              plot_freq = False, 
              hyper_parameters = {
                "n_neighbors": 3,
                "pca_dim": 4
                }
              ):
        SAMPLE_RATE = self.SAMPLE_RATE             # [Hz]. sampling rate.
        RECORD_SEC = recording_length               # [sec]. duration recording audio.

        LENGTH = SAMPLE_RATE * RECORD_SEC
        AMP_CONSTANT = self.AMP_CONSTANT
        print(f'Default Speaker: \n\t{sc.default_speaker()}')
        if plot_waveform:
            wplot = WaveformPlot(SAMPLE_RATE, LENGTH, AMP_CONSTANT)
            wplot.setup_fig()
            
        data = training_data
        print("Grabbing training data.")
        data = data.iloc[:len(training_labels)]
        data["training_labels"] = training_labels
        print("Initializing data...")
        analyzer = Analyzer(label_reference = mood_table, data=data, output_path="./data",num_cols=48)
        # libchroma = LibrosaChroma(SAMPLE_RATE)
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
            
            # data = mic.record(numframes=None)
            # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
            # while True:
            print("Recording data...")
            data_output = speaker.record(numframes=LENGTH)
            
            # Normalize the array by an integer, Resize it to fit the graph
            data_output_normal = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
            data_output_normal  = np.resize(data_output_normal, LENGTH)
            
            # wplot.draw(data_output_normal)
            data_output = np.ndarray.flatten(data_output)
            print(data_output, '\n', len(data_output))
            
            features = analyzer.analyze(raw_data=data_output)
            prediction = analyzer.predict["SVM"](features = features, pca_dim = hyper_parameters["pca_dim"])
            
            # visualizer = Visualizer()

            # visualizer.show(color = prediction["color"]["hex"])
            return prediction["color"]["rgb"]
    #libchroma.create_chroma(data_output)
    #libchroma.plot_chroma()
    
    
    

        
    # sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    
