import sys
import logging
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as ani
#from matplotlib import gridspec
#from matplotlib import dates as mdates
#from scipy.ndimage.filters import gaussian_filter1d

from StateData import StateData


ALL_STATE_DATA='data/all-states-daily.json'
COUNTRY_DATA='data/country-daily.json'
colors = ['blue', 'red', 'green', 'yellow', 'purple']

def banner():
    print('+========================================+')
    print('|    Animating State COVID Timelines     |')
    print('+========================================+')
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

def animate(i):
    color_count = 0
    plt.legend(names)
    for state in states:
        p = plt.plot(state.dates[:i], state.positive[:i])
        p[0].set_color(colors[color_count])
        color_count += 1
    ax = plt.gca()
#    for val in ax.get_yticks():
#        ax.axhline(y=val, linestyle='solid', linewidth=1, alpha=0.3,
#                   color='#dddddd', zorder=1)

banner()
logger = set_up_logger()

# Pick states that we should plot
names = []
if len(sys.argv)==1:
    names.append('WA')
else:
    for i in range(1,len(sys.argv)):
        names.append(sys.argv[i])

# Check if we want country data (special case)
states = []
for name in names:
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
    states.append(state)

# Normalize the dates so the days are plotting at the same time
earliest_state = min(states, key=lambda x:x.start_date)
logger.info(f"Normalizing Timelines to start on: {earliest_state.start_date}")
for s in states:
    diff = s.start_date - earliest_state.start_date
    additional_days = earliest_state.dates[:diff.days]
    new_dates = np.concatenate((additional_days, s.dates))
    s.dates = new_dates

    leading_zeros = np.zeros((len(additional_days),), dtype=int)
    new_data = np.concatenate((leading_zeros, s.positive))
    s.positive = new_data

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
plt.subplots_adjust(bottom = 0.2, top = 0.9)
plt.ylabel('Positive Cases')
plt.xlabel('Date')
plt.title("COVID Timeline")

animator = ani.FuncAnimation(fig, animate, interval = 150)
plt.show()

logger.info("plot-data Complete")

