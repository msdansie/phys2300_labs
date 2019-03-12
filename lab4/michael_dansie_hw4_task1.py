'''
Michael Dansie
PHYS 2300
Lab 4
3/11/2019
Assignment to learn how to interpolate data
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    wx_data = pd.read_csv(wx_file, usecols=[1, 3])#read in the data times and temps

    start_time = float_time(wx_data.at[0, 'Time'])#get initial time

    for index, row in wx_data.iterrows():#start the time at 0hrs
        wx_data.at[index, 'Time'] = float_time(wx_data.at[index, 'Time']) - start_time

        #replace garbage data and interpolate the missing value
        if index != 0 and index < len(wx_data['Ch1:Deg F']) - 1:
            if abs(wx_data.at[index, 'Ch1:Deg F']) < abs(wx_data.at[index + 1, 'Ch1:Deg F'])/3:
                wx_data.at[index, 'Ch1:Deg F'] = (wx_data.at[index-1, 'Ch1:Deg F'] + wx_data.at[index+1, 'Ch1:Deg F']) / 2

    #add the data to the dictionary
    harbor_data['wx_time'] = wx_data['Time']
    harbor_data['wx_temp'] = wx_data['Ch1:Deg F']
    
def float_time(string_time):
    """
    Takes in a time string 00:00:00 hours, minutes, seconds and converts to float
    :param string_time: a time in string format "00:00:00"
    :return: the same time in a float of hours
    """
    #convert minutes and seconds to hours and add them to the hours
    return float(string_time[0:2]) + float(string_time[3:5])/60 + float(string_time[6:8])/3600

def hour_time(hours, minutes, seconds):
    """
    Takes in hours, minutes, and seconds and creates a float time in hours
    :param hours: amount of hours
    :param minutes: amount of minutes
    :param seconds: amount of seconds
    :return: a float of the time in hours
    """
    #convert minutes and seconds to hours and add them to the hours
    return float(hours) + float(minutes)/60 + float(seconds)/3600

def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    #use to store the compiled times
    gps_times = []
    gps_data = pd.read_csv(gps_file, delimiter = "\t",  names = ['HOURS', 'MIN', 'SEC', 'ALT'], usecols = [0, 1, 2, 6], skiprows=2)#read in the hours, minutes, seconds, and altitudes
    start_time = hour_time(gps_data.at[0,'HOURS'], gps_data.at[0,'MIN'], gps_data.at[0,'SEC'])#get start time

    for index, row in gps_data.iterrows():#start times at 0hrs
        gps_times.append(hour_time(gps_data.at[index,'HOURS'], gps_data.at[index,'MIN'], gps_data.at[index,'SEC']) - start_time)

    #add the data to the dictionary
    harbor_data['gps_time'] = gps_times
    harbor_data['gps_alt'] = gps_data['ALT']

def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    #the time of ascent/descent change
    change_time = 0.0

    #calculate the last time of ascent
    for index, alt in enumerate(harbor_data['gps_alt']):
        if alt > harbor_data['gps_alt'][index + 1]:
            change_time = harbor_data['gps_time'][index]
            break
        
    #split up the temps by before and after change time, add to dictionary
    for index, time in enumerate(harbor_data['wx_time']):
        if(time > change_time):
            harbor_data['temp_up'] = harbor_data['wx_temp'][0:index]
            harbor_data['temp_down'] = harbor_data['wx_temp'][index:-1]
            break

    #split of the altitudes by before and after change time, add to dictionary
    for index, time in enumerate(harbor_data['gps_time']):
        if(time > change_time):
            harbor_data['alt_up'] = harbor_data['gps_alt'][0:index]
            harbor_data['alt_down'] = harbor_data['gps_alt'][index:-1]
            break

    #interpolate the alititudes of ascent and descent
    harbor_data['alt_up'] = np.linspace(harbor_data['alt_up'].iloc[0], harbor_data['alt_up'].iloc[-1], len(harbor_data['temp_up']))
    harbor_data['alt_down'] = np.linspace(harbor_data['alt_down'].iloc[0], harbor_data['alt_down'].iloc[-1], len(harbor_data['temp_down']))

def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    #first plot
    #temp vs time
    plt.figure()
    plt.subplot(2, 1, 1)                
    plt.title("Harbor Flight Data")
    plt.plot(harbor_data['wx_time'], harbor_data['wx_temp'])
    plt.ylabel("Temperature, F")
    
    #altitude vs time
    plt.subplot(2, 1, 2)
    plt.plot(harbor_data['gps_time'], harbor_data['gps_alt'])
    plt.ylabel("Altitude, ft")
    plt.xlabel("Mission Elapsed Time, Hours")
    plt.show()

    #second plot
    #ascent altitude vs temp
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("Harbor Ascent Flight Data")
    plt.plot(harbor_data['temp_up'], harbor_data['alt_up'])
    plt.ylabel("Altitude, ft")
    plt.xlabel("Temperature, F")

    #descent altitude vs temp
    plt.subplot(1, 2, 2)
    plt.title("Harbor Descent Flight Data")
    plt.plot(harbor_data['temp_down'], harbor_data['alt_down'])
    plt.xlabel("Temperature, F")
    plt.show()

def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = "TempPressure.Txt"
    gps_file = "GPSData.Txt"
    #wx_file = sys.argv[1]                   # first program input param
    #gps_file = sys.argv[2]                  # second program input param

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data

    #based on the last recorded altitude, remove garbage temperature data
    for index, time in enumerate(harbor_data['wx_time']):
        if time > harbor_data['gps_time'][-1]:
            harbor_data['wx_time'] = harbor_data['wx_time'][0:index]
            harbor_data['wx_temp'] = harbor_data['wx_temp'][0:index]
            break
    
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures

if __name__ == '__main__':
    main()
    exit(0)
