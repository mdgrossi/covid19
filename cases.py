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
urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/'
urlAtl = 'https://covidtracking.com/api/v1/states/'
byState = pd.read_csv(urlNYT+'us-states.csv', index_col='state',
                      parse_dates=['date'])
byCnty = pd.read_csv(urlNYT+'us-counties.csv', index_col='state',
                     parse_dates=['date'])
fullData = pd.read_csv(urlAtl+'daily.csv', index_col='state',
                       parse_dates=['date'])

# Areas of interest
regions = [('Florida', 'Miami-Dade'),
           ('Delaware', None),
           ('Massachusetts', 'Plymouth'),
           ('Michigan', 'Midland'),
           ('California', 'Placer'),
           ('Ohio', 'Montgomery'),
           ('Connecticut', 'Litchfield'),
           ('Rhode Island', None),
           ('Arkansas', 'Pulaski'),
           ('New York', 'Monroe')]
           
fontsize = 10
markersize = 2.5

for s,c in regions:
    
    # State data
    state = byState.loc[s]
    state = state.reset_index().set_index('date')
    state['newCases'] = state['cases'].diff()
    state['rolling14day'] = state['newCases'].rolling(14).mean()
    
    # Full data table of historic data
    historic = fullData.loc[abbr[s]]
    historic = historic.reset_index().set_index('date')
    
    # County data: total positive counts
    if c is not None:
        county = byCnty.loc[s]
        county = county.reset_index().set_index('county')
        county = county.loc[c]
        county = county.reset_index().set_index('date')
        county['newCases'] = county['cases'].diff()
        county['rolling14day'] = county['newCases'].rolling(14).mean()
    
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.4, 7.0), sharex=True)

        ax1.plot(state.newCases, '-o', color='black', markersize=markersize)
        ax1.plot(state['rolling14day'], linewidth=3, color='lightgrey')
        ax1.set_title('Daily New Confirmed Cases\n'\
                      'Data from https://github.com/nytimes/covid-19-data',
                      fontsize=fontsize+2)
        ax1.tick_params(axis='y', labelsize=12)
        ax1.set_ylabel(s, fontsize=fontsize)
        ax1.grid(b=True, which='major', axis='y', color='lightgrey')

        ax2.plot(county['newCases'], '-o', color='black', markersize=markersize)
        ax2.plot(county['rolling14day'], linewidth=3, color='lightgrey')
        ax2.set_xlabel('Date', fontsize=fontsize)
        ax2.tick_params(axis='x', labelsize=12, labelrotation=45)
        ax2.tick_params(axis='y', labelsize=12)
        ax2.set_ylabel('{} County'.format(c), fontsize=fontsize)
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax2.grid(b=True, which='major', axis='y', color='lightgrey')

        custom_lines = [plt.Line2D([0],[0], lw=1, markersize=markersize,
                                   color='black', marker='o'),
                        plt.Line2D([0],[0], lw=3, color='lightgrey')]
        ax2.legend(custom_lines, ['Daily count', '14-day moving average'],
                   ncol=2, fontsize=fontsize, edgecolor='lightgrey',
                   fancybox=True, shadow=True, loc='upper center',
                   bbox_to_anchor=(0.5, -0.32))
    
    # =================================================================== #
    # State data only (if no county provided)
    else:
        
        fig, ax = plt.subplots(1, 1, figsize=(5.4, 4.8))

        ax.plot(state['newCases'], '-o', color='black', markersize=markersize,
                label='Daily positive count')
        ax.plot(state['rolling14day'], linewidth=3, color='lightgrey',
                label='14-day moving average')
        ax.set_title('Daily New Confirmed Cases\n'\
                      'Data from https://github.com/nytimes/covid-19-data',
                      fontsize=fontsize+2)
        ax.tick_params(axis='x', labelsize=12, labelrotation=45)
        ax.tick_params(axis='y', labelsize=12)
        ax.set_xlabel('Date', fontsize=fontsize)
        ax.set_ylabel(s, fontsize=fontsize)
        ax.grid(b=True, which='major', axis='y', color='lightgrey')
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        custom_lines = [plt.Line2D([0],[0], lw=1, markersize=markersize,
                                   color='black', marker='o'),
                         plt.Line2D([0],[0], lw=3, color='lightgrey')]
        ax.legend(custom_lines, ['Daily count', '14-day moving average'],
                   ncol=2, fontsize=fontsize, edgecolor='lightgrey', 
                   fancybox=True, shadow=True, loc='upper center',
                   bbox_to_anchor=(0.5, -0.35))

    plt.tight_layout()        
    plt.savefig('/Users/mgrossi/Desktop/covid19/plots/covid19-{}.png'\
                .format(abbr[s]), dpi=175)

    # =================================================================== #
    # Daily positive counts normalized by daily test counts
    normalized = state.newCases/historic.totalTestResultsIncrease
    normalized.replace([np.inf, -np.inf], np.nan, inplace=True)
    firstDate = normalized.dropna().index[0] + pd.Timedelta(days=14)
    
    fig, ax = plt.subplots(1, 1, figsize=(5.4,  3.8))
    ax.plot(normalized.loc[firstDate:], '-o', color='black', 
            markersize=markersize, label='Normalized positive counts')
    ax.plot(normalized.rolling(14).mean(), linewidth=3, color='lightgrey',
            label='14-day moving average')
    ax.set_title('Daily New Confirmed Cases\nNormalized by Total Daily Tests\n'\
                  'Data from https://covidtracking.com',
                  fontsize=fontsize+2)
    ax.tick_params(axis='x', labelsize=12, labelrotation=45)
    ax.tick_params(axis='y', labelsize=12)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.set_xlabel('Date', fontsize=fontsize)
    ax.set_ylabel(s, fontsize=fontsize)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('/Users/mgrossi/Desktop/covid19/plots/normalized-{}.png'\
                .format(abbr[s]), dpi=175)
    