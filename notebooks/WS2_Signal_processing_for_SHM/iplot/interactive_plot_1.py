from iplot.utils import *
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
def plot_interactive():
    def duplicate_signal(signal,no_r=5):
        duplicate_signal = np.tile(signal, no_r)
        
        return duplicate_signal
    def make_sinoid(f,fs, duration):
        """
        Make a sine wave of a given frequency `f` with amplitude 1 and a given `duration` in seconds, sampled at frequency `fs`
        
        Returns;
        t      -  the timevector
        sinoid -  the sine wave
        """
        ### BEGIN SOLUTION
        t = np.arange(start=0, stop=duration, step=1/fs)
        sinoid = np.sin(2*np.pi*f*t) 
        ### END SOLUTION
        
        return t, sinoid

    def calc_spectrum(signal, fs):
        """
        Calculates the FFT spectrum of signal sampled at the frequency fs
        
        signal - the signal of which you want to calculate the fft spectrum
        fs  - the sampling frequency in Hz
        
        returns:
        fft_freq - the frequency vector
        fft_value - the results of the 
        
        """
        from numpy.fft import fft, fftfreq # We already imported the functions you'll need
        
        ### BEGIN SOLUTION
        
        # As a tip you can point people to google for the documentation
        fft_values = fft(signal)/fs # 
        fft_freq = fftfreq(len(signal), 1/fs) # NOTE: 1/fs!!! 
        
        ### END SOLUTION

        ## This additional step makes the plots look better, no need to worry about it :-)
        sorted_indices = np.argsort(fft_freq)
        fft_freq = fft_freq[sorted_indices]
        fft_values = fft_values[sorted_indices]
            
        return fft_freq, fft_values

    fs = 15 # Hz
    init_duration = 4
    no_samples = int(fs*init_duration)
    t_l, sin_l = make_sinoid(f=1, fs=fs, duration=100)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(t_l-2, sin_l, color='lightgray')
    line_tile, = ax[0].plot(t_l[:no_samples*5]-no_samples/fs, duplicate_signal(sin_l[:no_samples]), color='tab:orange', linewidth=1)
    line_w, = ax[0].plot(t_l[:no_samples], sin_l[:no_samples], color='tab:blue')

    ax[0].axvline(0, color='k', linestyle=':')
    line_ew = ax[0].axvline(no_samples/fs, color='k', linestyle=':')
    
    ax[0].set_xlim([-2,7])

    f_w, fft_s_w = calc_spectrum(sin_l[:no_samples], fs)

    line_s, = ax[1].plot(f_w, np.abs(fft_s_w), marker='x')
    ax[1].grid(which='both', linestyle=':')
    ax[1].set_ylabel('|X(f)|')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylim([0,3.5])
    
    plt.subplots_adjust(bottom=0.2)

        
    axc = plt.axes([0.25, 0.05, 0.65, 0.03])
    k_slider = Slider(
        ax=axc,
        label="Window length (s)",
        valmin=2,
        valmax=7,
        valinit=init_duration,
    )

    def update(fixed):
        no_samples = int(fs*k_slider.val)
        
        line_w.set_ydata(sin_l[:no_samples])
        line_w.set_xdata(t_l[:no_samples])
        
        line_tile.set_ydata(duplicate_signal(sin_l[:no_samples]))
        line_tile.set_xdata(t_l[:no_samples*5]-no_samples/fs)
        line_ew.set_xdata([no_samples/fs])
        
        f_w, fft_s_w = calc_spectrum(sin_l[:no_samples], fs)
        
        line_s.set_ydata(np.abs(fft_s_w))
        line_s.set_xdata(f_w)

        fig.canvas.draw_idle()

    # register the update function with each slider
    _ = k_slider.on_changed(update)
        