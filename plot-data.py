from sys import argv
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib import dates as mdates
from scipy.ndimage.filters import gaussian_filter1d
from scipy.misc import derivative
import datetime
import logging

WA_DATA='data/WA-data.json'
ALL_STATE_DATA='data/all-states-daily.json'

"""
#Setup Logger
logging.basicConfig(format='[%(levelname)s] %(message)s',
                    level=logging.INFO)
"""

class StateData:

    def __init__(self, name):
        self.name = name
        self.start_date = datetime.date.today()
        self.number_of_data_points = 0
        self.death    = np.array([])    
        self.positive = np.array([])    
        self.negative = np.array([])    
        self.total    = np.array([])
        self.dates    = np.array([])

    def set_number_of_data_points(self, num):
        self.number_of_data_points=num

    def set_start_date(self, date):
        self.start_date=date

    def append_death_value(self, value):
        self.death = np.append(self.death, [value])

    def append_positive_value(self, value):
        self.positive = np.append(self.positive, [value])

    def append_negative_value(self, value):
        self.negative = np.append(self.negative, [value])

    def append_total_value(self, value):
        self.total = np.append(self.total, [value])

    def append_date(self, int_date):
        year = int(str(int_date)[:4])
        month = int(str(int_date)[4:6])
        day = int(str(int_date)[6:8])
        self.dates = np.append(self.dates, [datetime.datetime(year,month,day)])

    def import_json(self, json_data):
        logging.info('Starting import_json')

        # Get expected number of data points. This is mainy just for 
        # sanity checks throught the code
        self.set_number_of_data_points(len(json_data))
        logging.info('Expected number of data points: %s',self.number_of_data_points)

        # Sort by date
        data=sorted(json_data, key=lambda k: k['date'])

        # Get start date
        d = data[0]['date']
        year = int(str(d)[:4])
        month = int(str(d)[4:6])
        day = int(str(d)[6:8])
        self.set_start_date(datetime.datetime(year, month, day))
        logging.info('Found start date: %s', self.start_date)

        for day in data:
            logging.debug(day)
            d = day.get('death', 0)
            p = day.get('positive', 0)
            n = day.get('negative', 0)
            t = day.get('total', 0)

            """
            pending = 0 if day['pending'] is None else day['pending']
            # Sanity check for totals
            if (p+n+pending) != t and day['date'] > 20200312:
                # For some reason deaths were included in total only up until
                # 2020-03-12
                logging.warning('Positive & Negative do not add up total on %s',
                                day['date'])
            """

            # Append data where it belongs
            self.append_death_value(d)
            self.append_positive_value(p)
            self.append_negative_value(n)
            self.append_total_value(t)
            self.append_date(day['date'])
    
        # Sanity check that there are the correct number of data points
        for a in (self.death, self.positive, self.negative, self.total):
            if len(a) != self.number_of_data_points:
                logging.warning("Incorrect number of data points: %s", a)

        # Somehow check that final data point is the correct date

        logging.info("Finished import_json Successfully")

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
    if len(argv)==1:
        name = 'WA'
    else:
        name = argv[1]
    state = StateData(name)

    logger.info(f"Extracting data for {state.name}")
    with open(ALL_STATE_DATA, 'r') as json_file:
        data = json.load(json_file)
    state_data = extract_single_state(data, state.name)
    
    logger.info("Importing state data")
    state.import_json(state_data)
    logging.info("Data has been imported, starting to plot")
    
    # Setup figure and grid
    fig = plt.figure(figsize=(13,6))
    gs = gridspec.GridSpec(2,2, height_ratios=[3,1])

    # Plot positive numbers (ax00)
    positive_smoothed = gaussian_filter1d(state.positive, sigma=2)
    ax00 = plt.subplot(gs[0,0])
    ax00.plot(state.dates, state.positive, 'b.-')
    ax00.plot(state.dates, positive_smoothed, 'b-.', lw=1)
    ax00.set_title('Positive Cases', weight='bold', fontsize=11)

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
        ax.tick_params(axis='x', labelrotation=70)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 2))

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

    fig.suptitle(f'{state.name} State COVID-19 Timeline', weight='bold', fontsize=17)
    plt.tight_layout()
    plt.show()
        
    logging.info("plot-data Complete")

if __name__=='__main__':
    main()
