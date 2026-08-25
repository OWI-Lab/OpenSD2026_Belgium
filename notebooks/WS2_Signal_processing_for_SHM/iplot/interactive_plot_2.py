
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
def plot_interactive():
    df = pd.read_csv('offshore_wind_data_rotor_stop.csv', header=0)
    f_s=25
    fa_rotor_stop = df['FA [g]'].iloc[22*f_s:350*f_s]
    t_rotor_stop = np.array(range(len(fa_rotor_stop)))/f_s
    w_n = 0.295 * 2 *np.pi # rad/s

    # Define initial parameters
    init_xi = 2

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()

    t = np.arange(start=0,stop=100,step=0.1)

    plt.plot(t_rotor_stop, fa_rotor_stop)
    line, = plt.plot(t_rotor_stop,np.exp(-init_xi/100*w_n*t_rotor_stop)*max(fa_rotor_stop), lw=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('h(t)')
    plt.grid(which='both', linestyle=':')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.25, bottom=0.4)



    axmass = plt.axes([0.25, 0.1, 0.65, 0.03])
    xi_slider = Slider(
        ax=axmass,
        label='Damping ratio $Xi$ (%)',
        valmin=0.01,
        valmax=3,
        valinit=init_xi,
    )




    # The function to be called anytime a slider's value changes
    def update(fixed):
        h = np.exp(-xi_slider.val/100*w_n*t_rotor_stop)*max(fa_rotor_stop)
        line.set_ydata(h)

        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    # register the update function with each slider
    xi_slider.on_changed(update)


    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        xi_slider.reset()
    button.on_clicked(reset)

    w = interact(update(fixed))