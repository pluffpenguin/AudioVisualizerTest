# This is it. The key library after going through so many different libraries/sources.
# pyaudio, pulseaudio, sounddevice, aslaaudio, pulsectl
import soundcard as sc
import soundfile as sf

import numpy as np
import matplotlib.pyplot as plt

from modules.analysis import AnalysisPlot
from modules.waveform_plot import WaveformPlot

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 8                  # [sec]. duration recording audio.

LENGTH = SAMPLE_RATE*RECORD_SEC
AMP_CONSTANT = 6000

print(f'Default Speaker: \n\t{sc.default_speaker()}')

wplot = WaveformPlot(LENGTH, AMP_CONSTANT)
wplot.setup_fig()

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
    
    # data = mic.record(numframes=None)
    # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
    # while True:
        
    data_output = speaker.record(numframes=LENGTH)
    # print(data, '\n', len(data))
    
    # Normalize the array by an integer, Resize it to fit the graph
    data_output = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
    data_output = np.resize(data_output, LENGTH)
    
    wplot.draw(data_output)    
        
        
input("Exit?")
        
    # sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    
