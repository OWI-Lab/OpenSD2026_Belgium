# Create the figure and the line that we will manipulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
def plot_interactive():
    df = pd.read_csv('./offshore_wind_turbine_parked.csv', header=0)
    df.head()

    def curve_fit_spatial(x_vals, mudline=-20):
        x_vals= np.append(x_vals,0)
        K = np.array([[(15-mudline)**2, (15-mudline)**3],[(69-mudline)**2, (69-mudline)**3],[(97-mudline)**2, (97-mudline)**3],[6*(97-mudline), 2]])
        theta = np.matmul(np.linalg.pinv(K), np.transpose(x_vals))

        y_vals = np.transpose(np.linspace(0,97-mudline))
        x_cf = theta[0]*y_vals**2+theta[1]*y_vals**3
        
        y_vals += mudline
        return y_vals, x_cf

    f_val_init = 0.25 # Hz
    fig, axes = plt.subplots(1,2, figsize=(9,5))
    f_s = 25
    f = np.fft.fftfreq(len(df['t [s]']), 1/f_s)
    f_ind = (np.abs(f - f_val_init)).argmin()

    FA_columns = [c for c in list(df.columns)[1:] if 'FA' in c]
    dots = []
    fft_dict = {}

    for c in FA_columns:
        X = np.fft.fft(df[c])
        fft_dict[c] = X
        fh = int(len(f)/2)
        axes[0].semilogy(f[:fh], np.abs(X[:fh]))

        dots.append(axes[1].plot(np.abs(X[f_ind]),int(c.split('LAT')[1][:3]), marker='o'))

            
    line = axes[0].axvline(x=f_val_init, linestyle='--', color='r')

    axes[0].set_xlim([0,2])
    axes[0].set_ylim([1e-3,1e2])

    axes[0].set_xlabel('Frequency (f)')
    axes[0].set_ylabel('|X(f)|')
    axes[0].grid(which='both', linestyle=':')

    axes[1].set_ylim([-20,100])
    axes[1].set_xlim([-1.1,1.1])

    cf = axes[1].plot([0,0],[-20,100], linestyle='--', color='k')




    axes[1].set_xlabel('ODS')
    axes[1].set_ylabel('Height (m)')
    axes[1].grid(which='both', linestyle=':')


    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.1, bottom=0.4)


        

    axmass = plt.axes([0.25, 0.1, 0.65, 0.03])
    f_slider = Slider(
        ax=axmass,
        label='f (Hz)',
        valmin=0,
        valmax=2,
        valinit=f_val_init,
    )



    # The function to be called anytime a slider's value changes
    def update(fixed):
        
        for c in FA_columns:

            f_ind = (np.abs(f - f_slider.val)).argmin()
            x_vals = []
            for c in  FA_columns:
                x_vals.append(np.real(fft_dict[c][f_ind]))
            
            max_idx = np.argmax(np.abs(x_vals))
            x_vals = np.array(x_vals)/x_vals[max_idx]
            y_cf, x_cf = curve_fit_spatial(x_vals)               
            for dot, x_val in zip(dots, x_vals):
                dot[0].set_xdata([x_val])
            
            cf[0].set_data(x_cf, y_cf)
    
        line.set_xdata([f_slider.val])
        """
        red_dot.set_ydata(np.abs(val))
        red_dot.set_xdata(f_slider.val)
        """
        fig.canvas.draw_idle()

    # register the update function with each slider
    f_slider.on_changed(update)


    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        f_slider.reset()
    button.on_clicked(reset)

    w = interact(update(fixed))
