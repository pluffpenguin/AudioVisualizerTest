import time
import wave
import struct
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

sd.default.samplerate = 44100

''' 
print_device_info(): 
    For loop to print the information of all the devices with output channels.
    If the device does NOT have an output stream, do not print.
'''
def print_device_info():
    for i in range( len(sd.query_devices()) ):
        device = sd.query_devices(i)
        if device["max_output_channels"] == 0: continue
        
        print('======================================================')
        print(f'{device["index"]}: {device["name"]}\n')
        for key, value in device.items():
            if key == 'name' or key == 'index': 
                continue
            print(f'  {key}: {value}')
        print()


print_device_info()


def audio_callback(indata, frames, time, status):
    print('Audio callback is being called!')
    """This is called (from a separate thread) for each audio block."""
    audio_data = np.copy(indata[:, 0])
    print(f'{status}\n')
    process_audio_data(audio_data)

def process_audio_data(data):
    print(data)
    print(f'Length of Data: {len(data)}')
    # Do something with the audio data, such as calculate the waveform
    # waveform = calculate_waveform(data)
    # # Plot the waveform
    # plot_waveform(waveform)

device_id = 8
chosen_device = sd.query_devices(device_id)

CHUNK = 1024*2

stream = sd.OutputStream(
    callback=audio_callback, 
    device=device_id,
    channels=chosen_device['max_output_channels'],
    samplerate=chosen_device['default_samplerate'],
    blocksize=CHUNK,
    dtype='float32',
    )
stream.start()

time.sleep(1/5)

stream.stop()
stream.close()