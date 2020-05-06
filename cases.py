#!/usr/bin/env python

# Import libraries
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from us_state_abbrev import us_state_abbrev as abbr

# Load data
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/'
byState = pd.read_csv(url+'us-states.csv', index_col='state',
                      parse_dates=['date'])
byCnty = pd.read_csv(url+'us-counties.csv', index_col='state',
                     parse_dates=['date'])

# Areas of interest
regions = [('Florida', 'Miami-Dade'),
           ('Delaware', None),
           ('Massachusetts', 'Plymouth'),
           ('Michigan', 'Midland'),
           ('California', 'Placer'),
           ('Ohio', 'Montgomery'),
           ('Connecticut', 'Litchfield'),
           ('Rhode Island', 'Providence')]

for s,c in regions:
    
    # State data
    state = byState.loc[s]
    state = state.reset_index().set_index('date')
    state['newCases'] = state['cases'].diff()
    state['rolling14day'] = state['newCases'].rolling(14).mean()
    
    # County data
    if c is not None:
        county = byCnty.loc[s]
        county = county.reset_index().set_index('county')
        county = county.loc[c]
        county = county.reset_index().set_index('date')
        county['newCases'] = county['cases'].diff()
        county['rolling14day'] = county['newCases'].rolling(14).mean()
    
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 8.0), sharex=True)

        ax1.plot(state.newCases, '-o', color='black')
        ax1.plot(state['rolling14day'], linewidth=3, color='lightgrey')
        ax1.set_title('Daily New Confirmed Cases\n'\
                      'Data from https://github.com/nytimes/covid-19-data',
                      fontsize=14)
        ax1.tick_params(axis='y', labelsize=12)
        ax1.set_ylabel(s, fontsize=12)
        # ax1.spines['top'].set_visible(False)
        # ax1.spines['right'].set_visible(False)
        ax1.grid(b=True, which='major', axis='y', color='lightgrey')

        ax2.plot(county['newCases'], '-o', color='black')
        ax2.plot(county['rolling14day'], linewidth=3, color='lightgrey')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.tick_params(axis='x', labelsize=12)
        ax2.tick_params(axis='y', labelsize=12)
        ax2.set_ylabel('{} County'.format(c), fontsize=12)
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        # ax2.spines['top'].set_visible(False)
        # ax2.spines['right'].set_visible(False)
        ax2.grid(b=True, which='major', axis='y', color='lightgrey')

        custom_lines = [plt.Line2D([0],[0], lw=1, color='black', marker='o'),
                        plt.Line2D([0],[0], lw=3, color='lightgrey')]
        ax2.legend(custom_lines, ['Daily count', '14-day moving average'],
                   ncol=2, fontsize=12, bbox_to_anchor=(0.9, -0.18),
                   edgecolor='lightgrey', fancybox=True, shadow=True)
    else:
        
        fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8))

        ax.plot(state['newCases'], '-o', color='black', label='Daily count')
        ax.plot(state['rolling14day'], linewidth=3, color='lightgrey',
                label='14-day moving average')
        ax.set_title('Daily New Confirmed Cases\n'\
                      'Data from https://github.com/nytimes/covid-19-data',
                      fontsize=14)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(s, fontsize=12)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.legend(loc='upper left')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(b=True, which='major', axis='y', color='lightgrey')

    plt.tight_layout()        
    plt.savefig('/Users/mgrossi/Desktop/covid19/plots/covid19-{}.png'\
                .format(abbr[s]), dpi=175)
