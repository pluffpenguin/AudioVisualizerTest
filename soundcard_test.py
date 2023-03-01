# This is it. The key library after going through so many different libraries/sources.
# pyaudio, pulseaudio, sounddevice, aslaaudio, pulsectl
import soundcard as sc
import soundfile as sf

import numpy as np
import matplotlib.pyplot as plt

from modules.waveform_plot import WaveformPlot
from modules.librosa_chroma import LibrosaChroma

# from modules.analysis import AnalysisPlot

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 10                  # [sec]. duration recording audio.

LENGTH = SAMPLE_RATE*RECORD_SEC
AMP_CONSTANT = 6000

print(f'Default Speaker: \n\t{sc.default_speaker()}')

# wplot = WaveformPlot(SAMPLE_RATE, LENGTH, AMP_CONSTANT)
# wplot.setup_fig()

libchroma = LibrosaChroma(SAMPLE_RATE)

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
    
    # data = mic.record(numframes=None)
    # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
    # while True:
    
    data_output = speaker.record(numframes=LENGTH)
    
    # Normalize the array by an integer, Resize it to fit the graph
    # data_output = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
    # data_output = np.resize(data_output, LENGTH)
    
    # wplot.draw(data_output)
    data_output = np.ndarray.flatten(data_output)
    print(data_output, '\n', len(data_output))
    
    libchroma.create_chroma(data_output)
    libchroma.plot_chroma()
    
    
    

        
    # sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    
