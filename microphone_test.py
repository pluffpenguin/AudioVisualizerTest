import pyaudio
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt

import time


# run with python3
# https://stackoverflow.com/questions/55143976/python-how-to-record-system-audiothe-output-from-the-speaker

CHUNK = 1024*2  # Record in CHUNKs of 1024 samples
SAMPLE_FORMAT = pyaudio.paInt16  # 16 bits per sample
CHANNELS = 1
FS = 44100  # Record at 44100 samples per second
SECONDS = 1
FILENAME = "C418_AriaMath.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

plt.xlabel('Chunk')
plt.ylabel('Integer')

def print_devices():
	print ( "Available devices:\n")
	for i in range(0, p.get_device_count()):
		info = p.get_device_info_by_index(i)
		print ( str(info["index"]) +  ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
		pass

# Change to your device ID
# 2, 4, 7, 8, 10, 23, 24, 26
device_id = 3
device_info = p.get_device_info_by_index(device_id)
# CHANNELS = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
# https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
stream = p.open(format=SAMPLE_FORMAT,
                channels=CHANNELS,
#                 rate=int(device_info["defaultSampleRate"]),
                rate=FS,
                input=True,
                frames_per_buffer=CHUNK,
#                 input_device_index=device_info["index"],
#                 as_loopback=True
                )

def get_data_int():
	data = stream.read(CHUNK)		 
	data_int = struct.unpack(str(CHUNK) + 'h', data)
	return data_int

def print_data_int(data_int):
	print(f'{data_int}')
	print(f'Length of Data: {len(data_int)}')

def close():
	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()



print_devices()


data_int = get_data_int()
fig, ax = plt.subplots()

ax.set_ylim(-6000, 6000)
ax.set_xlim(0, CHUNK)

ax.set_ylabel('Integer')
ax.set_xlabel('Chunk')


x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK), 'r')
line.set_color('blue')
fig.show()



# Actual code
running = True


while running:
	data_int = get_data_int()
	line.set_ydata(data_int)
	fig.canvas.draw()
	fig.canvas.flush_events()


# print(len(frames))


# frames = []  # Initialize array to store frames
# print('\nRecording', device_id, '...\n')


# capture chunk info for amount of seconds
# for i in range(0, int(FS / CHUNK * SECONDS)):
#     if not i == 42:
#         continue
#     
#     data = stream.read(CHUNK)
#     print(data)
#     frames.append(data)
#     print(f'Length of Data: {len(data)}')
#     data_int = struct.unpack(str(2*CHUNK) + 'B', data)
#     print(data_int)
