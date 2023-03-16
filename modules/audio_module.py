# This is it. The key library after going through so many different libraries/sources.
# pyaudio, pulseaudio, sounddevice, aslaaudio, pulsectl
import soundcard as sc
import soundfile as sf

import numpy as np

# from modules.waveform_plot import WaveformPlot

# from modules.analysis import AnalysisPlot

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 1/10                  # [sec]. duration recording audio.

LENGTH = int(SAMPLE_RATE*1/100)
AMP_CONSTANT = 6000

class AudioModule:
    def __init__(self, maxBrightness):
        self.speaker = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE)
        self.maxBrightness = maxBrightness
        self.maxAmpTemp = 0
        self.maxOverPeriod = 0
        self.maxCounter = 90 # resets to 0
        self.maxOverflow = 100
        print(f'> Audio Module Initialized: \n\t{sc.default_speaker()}')
    
    def maxCounterAddition(self):
        self.maxCounter += 1
        if self.maxCounter > self.maxOverflow:
            self.maxCounter = 0
            self.maxAmpTemp = self.maxOverPeriod
    
    def getAudioData(self, TARGET_LENGTH):
        if TARGET_LENGTH == None: # real time
            data_output = self.speaker.record(numframes=None)
            
            data_output = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
            data_output = np.resize(data_output, LENGTH)
            data_output = np.ndarray.flatten(data_output)
            
            data_max = np.max(data_output)
            if self.maxOverPeriod < data_max: 
                self.maxOverPeriod = data_max
            
            # add to the counter, changes max every 100 records
            self.maxCounterAddition()
            
            return data_output, data_max
        else: # not real time
            pass
        
    def getBrightnessInt(self):
        data_output, data_max = self.getAudioData()
        brightness = data_max/self.maxAmpTemp
        return int(brightness*255)
    



# with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
    
#     # data = mic.record(numframes=None)
#     # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
#     while True:
#         # data_output = speaker.record(numframes=LENGTH)
#         data_output = speaker.record(numframes=None)
        
#         # Normalize the array by an integer, Resize it to fit the graph
#         data_output = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
#         data_output = np.resize(data_output, LENGTH)
#         data_output = np.ndarray.flatten(data_output)
#         print(data_output, '\n', len(data_output))
    
    