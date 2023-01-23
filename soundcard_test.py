# This is it. The key library after going through so many different libraries/sources.
# pyaudio, pulseaudio, sounddevice, aslaaudio, pulsectl
import soundcard as sc
import soundfile as sf

import numpy as np

import matplotlib.pyplot as plt

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 1/10                  # [sec]. duration recording audio.

LENGTH = int(410)
AMP_CONSTANT = 6000

print(f'Default Speaker: \n\t{sc.default_speaker()}')

# Setting up for matplotlib
fig, ax = plt.subplots()

ax.set_ylim(-AMP_CONSTANT, AMP_CONSTANT)
ax.set_xlim(0, LENGTH)

ax.set_ylabel('Integer')
ax.set_xlabel('Chunk')

x = np.arange(0, 2 * LENGTH, 2)
line, = ax.plot(x, np.random.rand(LENGTH), 'r')
line.set_color('blue')
fig.show()

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker:
    
    # data = mic.record(numframes=None)
    # data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
    while True:
        data_output = speaker.record(numframes=LENGTH)
        # print(data, '\n', len(data))
        
        # Normalize the array by an integer, Resize it to fit the graph
        data_output = np.multiply(np.sum(data_output, axis=1), AMP_CONSTANT)
        data_output = np.resize(data_output, LENGTH)
        # print('Length ^', len(data))
        
        line.set_ydata(data_output)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    # sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.