from numpy import array, diff, where, split
from scipy import arange
import soundfile
import numpy, scipy
import pylab
import copy
import paho.mqtt.client as mqtt
import matplotlib
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

# OpenWeatherMap API: https://openweathermap.org/current

# TODO: Sign up for an API key
OWM_API_KEY = 'f13213863c21e47c195e834cdb8513e5'  # OpenWeatherMap API Key

DEFAULT_ZIP = 90089

def get_weather(zip_code):
    params = {
        'appid': OWM_API_KEY, 'zip': DEFAULT_ZIP, 'units': "imperial"
        # TODO: referencing the API documentation, add the missing parameters for zip code and units (Fahrenheit)
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        # TODO: Extract the temperature & humidity from data, and return as a tuple
        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        return(temp,hum)

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0
        
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    
    file_path = 'audiocheck.net_sin_1000Hz_-3dBFS_3s.wav'
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