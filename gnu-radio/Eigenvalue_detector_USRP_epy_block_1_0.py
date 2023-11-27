"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time
import matplotlib.pyplot as plt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vectorSize=2**14, Pfa=0.05, Smooth_fact=5, Threshold_corr=1,sampling_rate=30e3,num_channels=4,channel=0,noise_amplitude=0.1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Eigenvalue_detector_channels',
            in_sig=[(np.complex64,vectorSize)],
            out_sig=[(np.complex64,vectorSize), (np.float32,vectorSize)],
        )
        self.portName = 'messageOutput'
        self.message_port_register_out(pmt.intern(self.portName))
        self.vectorSize = vectorSize
        self.Pfa = Pfa
        self.Smooth_fact = Smooth_fact
        self.Threshold_corr = Threshold_corr
        self.sampling_rate=sampling_rate
        self.num_channels=num_channels
        self.channel=channel
        self.noise_amplitude=noise_amplitude=0.1
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #Hard-coding vaibles as program is buggy
        #Size of the FFT
        #vectorSize = 2**11
        Ns= self.vectorSize       
        signal=input_items[0][0]
        channel_outputs_size=int(self.vectorSize/self.num_channels)
        Ratio1=0
        gamma=0
        
        # Perform FFT of the combined signal
        fft_result = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(fft_result), 1.0 / self.sampling_rate)

        # Divide the spectrum into n equal channels
        n = int(self.num_channels) # Number of channels

        total_frequency_range = max(freq) - min(freq)
        channel_bandwidth = total_frequency_range / n

        # Define the center frequencies of the n channels
        center_frequencies = [min(freq) + (i + 0.5) * channel_bandwidth for i in range(n)]

        # Create channels for each frequency range
        channels = []
        for center_frequency in center_frequencies:
            channel = np.logical_and(freq >= center_frequency - channel_bandwidth / 2, freq < center_frequency + channel_bandwidth / 2)
            channels.append(channel)

        # Apply FFT results to each channel
        fft_channels = []
        for i in range(n):
            fft_channel = np.copy(fft_result)
            #white_noise = np.mean(np.abs(fft_result)) * np.random.randn(len(signal))
            fft_channel[~channels[i]] = 0  # Add white noise to frequencies outside of the channel
            #fft_channel=fft_channel+white_noise
            fft_channels.append(fft_channel)

        # Perform Inverse FFT on each channel
        reconstructed_signals = [np.fft.ifft(fft_channels[i]) for i in range(n)]
        noise_reconstructed=np.random.randn(len(reconstructed_signals[0]))*0.003
        reconstructed_signals=reconstructed_signals[:]+noise_reconstructed
        #signal=reconstructed_signals[int(self.channel)] 
        active_channel_list=[]
        for ii in range(n):
            signal=reconstructed_signals[ii]
          
            #Pfa = 0.05  # Probability of false alarm
            pd = 1 - self.Pfa

            # Tracey-Widom dist
            xi = np.array([-3.9, -3.18, -2.78, -1.91, -1.27, -0.59, 0.45, 0.98, 2.02])
            yi = np.array([0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99])

            # Find the index where the value in 'yi' is closest to 'pd'
            Tracy_Widom_table_index = np.argmin(np.abs(yi - pd))

            Tracy_Widom_value = xi[Tracy_Widom_table_index]

            # Number of transmitters and receivers
            M = 1
            P = 1

            N = 1
            L = self.Smooth_fact  # Smoothing factor

            # Finding the "smoothed" received signal
            #X_hat = np.zeros((M * L, Ns))
            #for k in range(L, Ns):
            #    for l in range(1, L + 1):
            #        X_hat[M * l - M:l * M, k] = signal[k - l + 1]
            
            X_hat = np.zeros((M*L,Ns-L))
            for k in range(0,L):
                X_hat[k,:] = signal[L-k:Ns-k]
                
            
            R = np.matmul(X_hat, np.transpose(X_hat))
            R /= Ns

            # Eigenvalues
            EIG = np.linalg.eigvals(R)
            Lambda_max = max(EIG)
            Lambda_min = min(abs(EIG))
#             print("Max eigenvalue: ", Lambda_max)
#             print("Min eigenvalue: ", Lambda_min)
            
            if Lambda_min==0:
                detected_signal="Detected signal(eigenvalue is zero)"
                active_channel_list.append("1")                
            else:
                
               # Finds Ratio for MME Detection
               Ratio1 = Lambda_max / Lambda_min

               # Find Ratio for EME Detection
               # Ratio2 = AVG_PWR / Lambda_min
               # Find threshold
               A = np.sqrt(Ns) + np.sqrt(M * L)
               B = np.sqrt(Ns) - np.sqrt(M * L)
               C = Ns * M * L
               r1 = (A**2) / (B**2)
               r2 = 1 + (A**(-2/3) / C**(1/6)) * Tracy_Widom_value
               gamma = self.Threshold_corr*(r1 * r2)
               if gamma <=Ratio1:
                  detected_signal="Detected signal"
                  active_channel_list.append("1")
                  for vectorIndex in range(len(output_items[1])):
                      for sampleIndex in list(range(channel_outputs_size*ii, channel_outputs_size*(ii+1))):
                        output_items[1][vectorIndex][sampleIndex] = 20.0
               else:
                  detected_signal="No signal"
                  active_channel_list.append("0")
                  for vectorIndex in range(len(output_items[1])):
                      for sampleIndex in list(range(channel_outputs_size*ii, channel_outputs_size*(ii+1))):
                        output_items[1][vectorIndex][sampleIndex] = 0.01
                
            if int(self.channel)==ii:
                print("The ratio for selected channel is: ",Ratio1)
                print("The threshold is:", gamma)
            
                             
                


    #         # Convert the signal array to a string
    #         signal_str = ' '.join(map(str, signal))
    #         
    #         # Create a dictionary to hold both pieces of information
    #         message_data = {'signal': signal_str, 'detected_signal': detected_signal}
    #         print("Lambda_min:", Lambda_min)
    #         print("Ratio1:", Ratio1)
            #Printing:
#                print("Ratio: ", Ratio1)
#                print("Gamma: ",gamma)
#                print(detected_signal)
        # Convert the dictionary to a PMT message
        compound_message = pmt.to_pmt(active_channel_list)
        #output_items[0][0]=reconstructed_signals[int(self.channel)]
        # Publish the compound message
        self.message_port_pub(pmt.intern(self.portName), compound_message)
        return len(output_items[0])




