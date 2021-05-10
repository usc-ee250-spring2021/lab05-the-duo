from numpy import array, diff, where, split
from scipy import arange
import soundfile
import numpy, scipy
import pylab
import copy
import paho.mqtt.client as mqtt
import matplotlib
import freesound
import time
matplotlib.use('tkagg')
#oOjuR3yG4igtZPPNJMefuAdxRR7meFW32E6gL2Bo
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def findPeak(magnitude_values, noise_level=2000):
   
    splitter = 0
    # zero out low values in the magnitude array to remove noise (if any)
    magnitude_values = numpy.asarray(magnitude_values)        
    low_values_indices = magnitude_values < noise_level  # Where values are low
    magnitude_values[low_values_indices] = 0  # All low values will be zero out
   
    indices = []
   
    flag_start_looking = False
   
    both_ends_indices = []
   
    length = len(magnitude_values)
    for i in range(length):
        if magnitude_values[i] != splitter:
        #if magnitude_values.any() != splitter:
            if not flag_start_looking:
                flag_start_looking = True
                both_ends_indices = [0, 0]
                both_ends_indices[0] = i
        else:
            if flag_start_looking:
                flag_start_looking = False
                both_ends_indices[1] = i
                # add both_ends_indices in to indices
                indices.append(both_ends_indices)
               
    return indices

def extractFrequency(indices, freq_threshold=2):
   
    extracted_freqs = []
   
    for index in indices:
        freqs_range = freq_bins[index[0]: index[1]]
        avg_freq = round(numpy.average(freqs_range))
       
        if avg_freq not in extracted_freqs:
            extracted_freqs.append(avg_freq)

    # group extracted frequency by nearby=freq_threshold (tolerate gaps=freq_threshold)
    group_similar_values = split(extracted_freqs, where(diff(extracted_freqs) > freq_threshold)[0]+1 )
   
    # calculate the average of similar value
    extracted_freqs = []
    for group in group_similar_values:
        extracted_freqs.append(round(numpy.average(group)))
   
    print("freq_components", extracted_freqs)
    return extracted_freqs
import requests

def dnld(link):
    import os
    filename = link.split('/')[-3]
    os.system(f"wget --content-disposition '{link}' --header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header 'Connection: keep-alive' --header 'Cookie: csrftoken=gqFF89vNe2UTHlN4Nih9KQMZPVR7qpm1g9B7gT0pdMW6QmIG61uFkbvYQFRFfFCd; sessionid=msmgu0qhfx8aooucdo42eqsik03xlv5k' --header 'Upgrade-Insecure-Requests: 1'")
    #print(filename)

__token = "oOjuR3yG4igtZPPNJMefuAdxRR7meFW32E6gL2Bo"

from glob import glob
import os

if __name__ == '__main__':
    
    allwav = glob('*.wav')
    for f in allwav:
        os.remove(f)
        
    # ask user for query
    val = input("What frequency do you want the note to be in (Hz)?")

    client = freesound.FreesoundClient()
    client.set_token(__token,"token")

    #results = client.text_search(query="440Hz",filter="type:wav duration:3",sort = "score", group_by_pack = 0, fields = "download")
    results = client.text_search(query=str(val),filter="type:wav duration:3",sort = "score", group_by_pack = 0, fields = "download")
    print(dir(results))
    print(results.results)
        
    for sound in results:
        #sound.retrieve_preview(".",sound.download+".wav")
        print(sound.download)
        dnld(sound.download)
    #print(sound.download)
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
   
    #file_path = 'audiocheck.net_sin_1000Hz_-3dBFS_3s.wav'
    #file_path = '562238__anonio82__square.wav'

    file_path = glob('*square.wav')[0]
    #file_path = client.text_search(original_filename=
    print('Open audio file path:', file_path)
   
    audio_samples, sample_rate  = soundfile.read(file_path, dtype='int16')
    number_samples = len(audio_samples)
    print('Audio Samples: ', audio_samples)
    print('Number of Sample', number_samples)
    print('Sample Rate: ', sample_rate)
   
    # duration of the audio file
    duration = round(number_samples/sample_rate, 2)
    print('Audio Duration: {0}s'.format(duration))
   
    # list of possible frequencies bins
    freq_bins = arange(number_samples) * sample_rate/number_samples
    print('Frequency Length: ', len(freq_bins))
    print('Frequency bins: ', freq_bins)
   
#     # FFT calculation
    fft_data = scipy.fft(audio_samples)
    print('FFT Length: ', len(fft_data))
    print('FFT data: ', fft_data)

    freq_bins = freq_bins[range(number_samples//2)]      
    normalization_data = fft_data/number_samples
    magnitude_values = normalization_data[range(len(fft_data)//2)]
    magnitude_values = numpy.abs(magnitude_values)
       
    indices = findPeak(magnitude_values=magnitude_values, noise_level=200)
    frequencies = extractFrequency(indices=indices)
    print("frequencies:", frequencies)
    note_produced = frequencies[0]
    client.publish("theduo/lcd", note_produced)
    print(note_produced)
   
    x_asis_data = freq_bins
    y_asis_data = magnitude_values
 
    pylab.plot(x_asis_data, y_asis_data, color='blue') # plotting the spectrum
 
    pylab.xlabel('Freq (Hz)')
    pylab.ylabel('|Magnitude - Voltage  Gain / Loss|')
    pylab.show()

    #main(sys.argv[1])
    while True:
        #print("delete this line")
        time.sleep(1)
