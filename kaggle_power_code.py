# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:36:17 2020

@author: hboateng
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import datetime
 
### IMPORTING TXT FILE
power = pd.read_csv('household_power_consumption.txt', header = 0,
                    delimiter=';')

#Set date and time to date_time dtypes
power['Date'] = pd.to_datetime(power['Date'], yearfirst = True)
power['Time'] = pd.to_datetime(power['Time'])

#create df with all values to numbers, errors as NaN
power_num = power.apply(pd.to_numeric, errors ='coerce')

#copy numbers to new columns as floats as df.groupby can't handle decimals
power_num['Gap'] = power_num['Global_active_power'].astype(float)
power_num['Grp'] = power_num['Global_reactive_power'].astype(float)
power_num['V'] = power_num['Voltage'].astype(float)
power_num['Gi'] = power_num['Global_intensity'].astype(float)
power_num['Sub_1'] = power_num['Sub_metering_1'].astype(float)
power_num['Sub_2'] = power_num['Sub_metering_2'].astype(float)
power_num['Sub_3'] = power_num['Sub_metering_3'].astype(float)

#split date and time from original, float columns from copy and join
power_a = power[['Date', 'Time']].copy()
power_b = power_num[['Gap', 'Grp', 'V', 'Gi', 'Sub_1', 'Sub_2', 'Sub_3']].copy()
#check power_a and power_b are same length
if power_a.shape[0] == power_b.shape[0]:
    power_times = power_a.join(power_b)

#group by time
power_times = power_times.groupby('Time').mean().reset_index()

pdfname='multipage_pdf_'+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.pdf'

#create pdf
with PdfPages(pdfname) as pdf:
    # Create axes
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8.27,11.69))
    fig.suptitle("1", fontsize=16)
    myFmt = mdates.DateFormatter('%H:%M')

    ax1.plot(power_times['Time'], power_times['Grp'])
    ax1.xaxis.set_major_formatter(myFmt)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Grp')

    ax2.plot(power_times['Time'], power_times['V'])
    ax2.xaxis.set_major_formatter(myFmt)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('V')

    ax3.plot(power_times['Time'], power_times['Gi'])
    ax3.xaxis.set_major_formatter(myFmt)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Gi')

    pdf.savefig(fig)
    plt.close()

    ### Create axes
    fig, (ax4, ax5, ax6) = plt.subplots(3,1, figsize=(8.27,11.69))
    fig.suptitle("2", fontsize=16)

    ax4.plot(power_times['Time'], power_times['Sub_1'])
    ax4.xaxis.set_major_formatter(myFmt)
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Sub_2')

    ax5.plot(power_times['Time'], power_times['Sub_2'])
    ax5.xaxis.set_major_formatter(myFmt)
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Sub_2')


    ax6.plot(power_times['Time'], power_times['Sub_3'])
    ax6.xaxis.set_major_formatter(myFmt)
    ax6.set_xlabel('Time')
    ax6.set_ylabel('Sub_3')

    pdf.savefig(fig)
    plt.close()
