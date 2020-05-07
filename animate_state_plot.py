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
    p = plt.plot(state.dates[:i], state.positive[:i])
    p[0].set_color('green')

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

# Setup figure
#fig, ax = plt.subplots()
#xdata, ydata = [], [] 
#line, = plt.plot([], [], 'ro')

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
plt.subplots_adjust(bottom = 0.2, top = 0.9)
plt.ylabel('Y-label')
plt.xlabel('X-label')
plt.title("Animating Graphs")

animator = ani.FuncAnimation(fig, animate, interval = 200)
plt.show()

logger.info("plot-data Complete")

