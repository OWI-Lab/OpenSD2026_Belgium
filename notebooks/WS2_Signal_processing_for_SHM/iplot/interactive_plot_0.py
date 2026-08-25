from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
import numpy as np
from iplot.utils import *
# Define initial parameters
def plot_interactive():
    f = 0.2
    fs=10

    init_f = 0.3
    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()

    t = np.arange(start=0, stop=10,step=1/100)
    h = np.sin(2*np.pi*f*t)
    line, = plt.plot(t,h, lw=2, color='gray')
    line2, = plt.plot(t,h, lw=1, color='tab:orange', marker='.', linestyle='-')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Signal(t)')
    plt.grid(which='both', linestyle=':')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.25, bottom=0.4)


    axmass = plt.axes([0.3, 0.15, 0.55, 0.03])
    f_slider = Slider(
        ax=axmass,
        label='Signal frequency (Hz)',
        valmin=0.1,
        valmax=2,
        valinit=f,
    )
    axstifness=plt.axes([0.3, 0.1, 0.55, 0.03])
    fs_slider = Slider(
        ax=axstifness,
        label="Sample Frequency (Hz)",
        valmin=1,
        valmax=20,
        valinit=fs,
    )


    # The function to be called anytime a slider's value changes
    def update(fixed):
        t = np.arange(start=0, stop=10,step=1/100)
        t_s= np.arange(start=0,stop=10,step=1/fs_slider.val)
        h = np.sin(2*np.pi*f_slider.val*t)
        h_s =np.sin(2*np.pi*f_slider.val*t_s)
        
        line.set_ydata(h)
        line2.set_data((t_s, h_s))

        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    # register the update function with each slider
    f_slider.on_changed(update)
    fs_slider.on_changed(update)


    w = interact(update(fixed))