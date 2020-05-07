import sys
import logging
import json
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib import dates as mdates
from scipy.ndimage.filters import gaussian_filter1d
import numpy as np

from StateData import StateData


ALL_STATE_DATA='data/all-states-daily.json'
COUNTRY_DATA='data/country-daily.json'

def banner():
    print('+=======================================+')
    print('|    Plotting State COVID Timelines     |')
    print('+=======================================+')
    print()

def set_up_logger():
    logging.basicConfig(format='[%(levelname)s] %(message)s')

    logger = logging.getLogger('COVID-Plotting')
    logger.setLevel(logging.DEBUG)
    return logger

def extract_single_state(data, state_name):
    state_data = []
    for d in data:
        if d['state'] == state_name:
            state_data.append(d)
    return state_data

def main():
    banner()
    logger = set_up_logger()

    # Pick state that we should plot
    if len(sys.argv)==1:
        name = 'WA'
    else:
        name = sys.argv[1]

    # Check if we want country data (special case)
    state = StateData(name)
    if name == "US":
        logger.info(f"Extracting data for the US")
        logger.info(f"Data file: {COUNTRY_DATA}")
        with open(COUNTRY_DATA, 'r') as json_file:
            state_data = json.load(json_file)
    else:
        logger.info(f"Extracting data for {state.name}")
        logger.info(f"Data file: {ALL_STATE_DATA}")
        with open(ALL_STATE_DATA, 'r') as json_file:
            data = json.load(json_file)
        state_data = extract_single_state(data, state.name)
    
    logger.info("Importing data")
    state.import_json(state_data)
    logger.info(f"Start Date: {state.start_date}")
    logger.info(f"{state.number_of_data_points} days imported")
    
    # Setup figure and grid
    fig = plt.figure(figsize=(13,6))
    gs = gridspec.GridSpec(2,2, height_ratios=[3,1])

    # Plot positive numbers (ax00)
    positive_smoothed = gaussian_filter1d(state.positive, sigma=2)
    ax00 = plt.subplot(gs[0,0])
    ax00.plot(state.dates, state.positive, 'b.-')
    ax00.plot(state.dates, positive_smoothed, 'b-.', lw=1)
    ax00.set_title('Positive Cases', weight='bold', fontsize=11)
    ax00.axes.get_xaxis().set_visible(False)

    #Plot positive rate of change (ax10)
    diff=np.diff(np.insert(state.positive, 0, 0, axis=0))
    diff_smoothed=gaussian_filter1d(diff, sigma=2)
    ax10 = plt.subplot(gs[1,0])
    ax10.plot(state.dates, diff, 'g.-')
    ax10.plot(state.dates, diff_smoothed, 'g-.', lw=1)
    ax10.set_title('Change per Day', weight='bold', fontsize=11)

    # Plot deaths (ax01)
    death_smoothed = gaussian_filter1d(state.death, sigma=2)
    ax01 = plt.subplot(gs[0,1])
    ax01.plot(state.dates, state.death, 'r.-', label='Death')
    ax01.plot(state.dates, death_smoothed, 'r-.', lw=1)
    ax01.set_title('Deaths', weight='bold', fontsize=11)
    ax01.axes.get_xaxis().set_visible(False)

    #Plot death rate of change (ax11)
    diff=np.diff(np.insert(state.death, 0, 0, axis=0))
    diff_smoothed=gaussian_filter1d(diff, sigma=2)
    ax11 = plt.subplot(gs[1,1])
    ax11.plot(state.dates, diff, 'g.-')
    ax11.plot(state.dates, diff_smoothed, 'g-.', lw=1)
    ax11.set_title('Change per Day', weight='bold', fontsize=11)


    # Things to set for each Plot
    for ax in ax00,ax01,ax10,ax11:
        # Asix setup
        y_vals = ax.get_yticks()
        for val in y_vals:
            ax.axhline(y=val, linestyle='solid', linewidth=1, alpha=0.3,
                       color='#dddddd', zorder=1)
        ylim=ax.set_ylim(bottom=0)
        xlim=ax.set_xlim(state.dates[0])
        formatter = mdates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)
        ax.tick_params(axis='x', labelrotation=45)
        ax.ticklabel_format(axis='y', style='plain')
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 7))

        # Important dates
        """
        # March 16th, Bar's & Restaurants are closed
        xloc=state.dates[12]
        ax.axvline(x=xloc)
        ax.text(xloc,1, 'Restaurants Close', fontsize=6,rotation=40)
        # March 17th, state schools closed
        xloc=state.dates[13]
        ax.axvline(xloc)
        ax.text(xloc,1, 'Schools Close', fontsize=6,rotation=40)
        # March 23rd, Gov. gives stay at home mandate
        xloc=state.dates[19]
        ax.axvline(xloc)
        ax.text(xloc,1, 'Stay-at-Home', fontsize=6,rotation=40)
        # March 27th, $2 trillion stimulus bill based
        xloc=state.dates[23]
        ax.axvline(xloc)
        ax.text(xloc,1, 'Stimulus Bill', fontsize=6,rotation=40)
        """

    fig.suptitle(f'{state.name} COVID-19 Timeline', weight='bold', fontsize=17)
    plt.tight_layout()
    if len(sys.argv) == 3 and sys.argv[2] == '--save':
        logger.info(f"Saving {state.name} plot in 'State-Timelines'")
        plt.savefig(f"State-Timelines/{state.name}-COVID-Timeline.png",
                    dpi=150)
    else:
        logger.info("Plotting")
        plt.show()
        
    logger.info("plot-data Complete")

if __name__=='__main__':
    main()
