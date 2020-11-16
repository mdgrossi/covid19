#!/usr/bin/env python

# Import libraries
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from scipy.interpolate import make_interp_spline, BSpline
from us_state_abbrev import us_state_abbrev as abbr

# Load data
urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/'
urlAtl = 'https://covidtracking.com/api/v1/states/daily.csv'
urlR0 = 'https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv'
byState = pd.read_csv(urlNYT+'us-states.csv', index_col='state',
                      parse_dates=['date'])
byCnty = pd.read_csv(urlNYT+'us-counties.csv', index_col='state',
                     parse_dates=['date'])
fullData = pd.read_csv(urlAtl, index_col='state', parse_dates=['date'])
Rnought = pd.read_csv(urlR0, index_col='region', parse_dates=['date'])

# Areas of interest
regions = [('Florida', 'Miami-Dade'),
           ('Delaware', None),
           ('Massachusetts', 'Plymouth'),
           ('Michigan', 'Midland'),
           ('California', 'Placer'),
           ('Ohio', 'Montgomery'),
           ('Connecticut', 'Litchfield'),
           ('Rhode Island', None),
           ('New York', 'Monroe'),
           ('North Carolina', 'Guilford'),
           ('Arkansas', 'Pulaski')]
           
fontsize = 10
markersize = 2.5

# Add r_e
def add_r0(fontsize=11):
    # Conditional coloring for prediction bar
    def color():
        return 'darkgreen' if re < 1 else 'darkred'
    # Legend location
    re = np.round(Re['mean'].iloc[-1], 2)
    ax.annotate('Effective reproduction', (100, 155), (100, 155), # was 180
                xycoords='axes points', fontsize=fontsize-2)
    ax.annotate(r'number: $r_e$ =', (100, 143), (100, 143),
                xycoords='axes points', fontsize=fontsize-2)
    ax.annotate(re, (160, 143), (160, 143),
                xycoords='axes points', fontsize=fontsize-2,
                color=color())
 
# Regional plots
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

        ax1.plot(state['newCases'], '-o', color='black', markersize=markersize)
        ax1.plot(state['rolling14day'], linewidth=3, color='lightgrey')
        thruDate = state['newCases'].index[-1].strftime('%B %d')
        ax1.set_title('Daily New Confirmed Cases through {}\n'\
                      'Data from https://github.com/nytimes/covid-19-data'\
                      .format(thruDate), fontsize=fontsize+2)
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
        thruDate = state['newCases'].index[-1].strftime('%B %d')
        ax.set_title('Daily New Confirmed Cases through {}\n'\
                      'Data from https://github.com/nytimes/covid-19-data'\
                      .format(thruDate), fontsize=fontsize+2)
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
    plt.close('all')

    # =================================================================== #
    # Percent of positive cases
    
    # Calculate percentages
    # Sort, interpolate NAs produced from divide by zero
    dailyPercent = historic.positiveIncrease/historic.totalTestResultsIncrease
    dailyPercent = dailyPercent[::-1].dropna()
    # Replace inf, -inf with 0 (Needed for Arkansas)
    dailyPercent.replace({-np.inf: 0, np.inf: 0}, inplace=True)
    newTimes = pd.date_range(dailyPercent.index[0], dailyPercent.index[-1],
                             freq='1H')
    spl = make_interp_spline(dailyPercent.index, dailyPercent, k=3)
    dailyPercentSmooth = pd.Series(spl(newTimes), index=newTimes)
    
    totalPercent = historic.positive/historic.totalTestResults
    totalPercent = totalPercent[::-1].dropna()
    spl = make_interp_spline(totalPercent.index, totalPercent, k=3)
    totalPercentSmooth = pd.Series(spl(newTimes), index=newTimes)
    #firstDate = totalPercentSmooth.index[0] + pd.Timedelta(days=14)
    firstDate = totalPercentSmooth.index[-1] - pd.Timedelta(days=60)
    
    # Effective reproduction rate
    Re = Rnought.loc[abbr[s]]
    
    fig, ax = plt.subplots(1, 1, figsize=(5.4,  4.8))
    ax.plot(dailyPercentSmooth.loc[firstDate:], linewidth=1, color='lightgrey',
            label='Daily positive cases')
    # ax.plot(totalPercentSmooth, linewidth=2, color='darkblue',
    #         label='Rolling total')
    ax.plot(dailyPercentSmooth.rolling(14*24).mean().loc[firstDate:], 
            linewidth=2, color='darkred', label='14-day moving avg.')
    ax.plot(dailyPercentSmooth.rolling(7*24).mean().loc[firstDate:], 
            linewidth=2, color='darkblue', label='7-day avg.')
    thruDate = dailyPercentSmooth.index[-1].strftime('%B %d')        
    ax.set_title('{} Daily Percentage of Positive Tests through {}\n'\
                 'Data from https://covidtracking.com & '\
                 'https://rt.live'.format(s, thruDate), fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=12, labelrotation=45)
    ax.tick_params(axis='y', labelsize=12)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    ax.set_xlabel('Date', fontsize=fontsize)
    ax.set_ylabel(s, fontsize=fontsize)
    ax.set_ylim(0, min(ax.get_ylim()[1],0.5))
    leg = ax.legend(loc='lower left', bbox_to_anchor=(0, -0.5), ncol=3, 
                    fontsize=fontsize-2, fancybox=True, shadow=True)
    add_r0()
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    fig.savefig('/Users/mgrossi/Desktop/covid19/plots/normalized-{}.png'\
                .format(abbr[s]), dpi=175, bbox_inches='tight')
    plt.close('all')
    
    if s == 'Florida':
        fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8))
        ax.plot(dailyPercentSmooth, label='Daily positive cases', 
                color='lightgrey', linewidth=1,)
        ax.plot(dailyPercentSmooth.rolling(14*24).mean(), color='darkred',
                linewidth=2, label='14-day moving avg.')
        ax.plot(dailyPercentSmooth.rolling(7*24).mean(), color='darkblue',
                linewidth=2, label='7-day moving avg.')
        thruDate = dailyPercentSmooth.index[-1].strftime('%B %d')
        ax.set_title('{} Daily Percentage of Positive Tests through {}\n'\
                     'Data from https://covidtracking.com & '\
                     'https://rt.live'.format(s, thruDate), fontsize=fontsize)
        leg = ax.legend(loc='lower left', bbox_to_anchor=(0.05, -0.4), ncol=3, 
                        fontsize=fontsize-2, fancybox=True, shadow=True)
        add_r0()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
        ax.tick_params(axis='x', labelsize=fontsize, labelrotation=45)
        ax.set_xlabel('Date', fontsize=fontsize)
        ax.set_ylabel('Percent', fontsize=fontsize)
        ax.set_ylim(0, 0.35)
        ax.grid(axis='y', alpha=0.25)
        plt.tight_layout()
        plt.savefig('/Users/mgrossi/Desktop/covid19/plots/FL_full_tseries.png',
                    dpi=175, bbox_inches='tight')
        
# =========================================================================== #