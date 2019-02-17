'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: three lists. One list with the information from the third column (date)
                        One list with only the years of the dates
                        One list with the information from the fourth column (temperature)
    """
    wyear = []
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperarture data
    wrecords = []

    with open(infile, mode='r') as file:
        
        file.readline()

        for rec in file:
            wrecords.append(rec.split())

    for row in wrecords:
        wdates.append(row[2])
        wtemperatures.append(float(row[3]))
        
        if row[2][0:4] not in wyear:
            wyear.append(float(row[2][0:4]))
    
    return wdates, wtemperatures, wyear


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    month = 1
    means = []
    std_dev = []

    while(month <= 12):
        sum = 0.0
        month_temps = []
        

        if(month < 10):
            check_month = "0" + str(month)
        else:
            check_month = str(month)
        
        for index, date in enumerate(wdates):
            if(date[4:6] == check_month):
                
                sum = sum + wtemp[index]
                month_temps.append(wtemp[index])
        
        means.append(sum / len(month_temps))
        std_dev.append(np.std(month_temps))
        
        month = month + 1

    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(xxx):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: xxx??
    """
    pass


def main(infile):
    weather_data = infile    # take data file as input parameter to file
    wdates, wtemperatures, wyear = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    plot_data_task1(wyear, wtemperatures, month_mean, month_std)
    # TODO: Create the data you need for this
    # plot_data_task2(xxx)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    #'data/CDO6674605799016.txt' = sys.argv[0]
    main("data/CDO6674605799016.txt")
    #exit(0)
