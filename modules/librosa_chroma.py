import numpy as np
import matplotlib.pyplot as plt

import librosa
import librosa.display

class LibrosaChroma:
    def __init__(self, SAMPLE_RATE) -> None:
        self.SAMPLE_RATE = SAMPLE_RATE
        
    def create_chroma(self, data_output):
        self.S = np.abs(librosa.stft(data_output))
        self.chroma = librosa.feature.chroma_stft(S=self.S, sr=self.SAMPLE_RATE) 
        
    def plot_chroma(self):
        fig, ax = plt.subplots(nrows=2, sharex=True)
        img = librosa.display.specshow(librosa.amplitude_to_db(self.S, ref=np.max),
                                    y_axis='log', x_axis='time', ax=ax[0])
        fig.colorbar(img, ax=[ax[0]])
        ax[0].label_outer()
        img = librosa.display.specshow(self.chroma, y_axis='chroma', x_axis='time', ax=ax[1])
        fig.colorbar(img, ax=[ax[1]])