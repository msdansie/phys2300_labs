'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: michael_dansie_hw3_task1&2.py

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

def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: five lists. One list with the information from the third column (date)
                        One list with only the years of the dates
                        One list of unique years
                        One list with the information from the fourth column (temperature)
                        One list with the yearly records from the twelfth column (max temperatures)
                        One list with the yearly records from the thirteenth column (min temperatures)
    """
    wyear = [] #list of years
    wdates = [] #list of dates
    wtemperatures = [] #list of temperatures
    wmax_temps = [] #list of yearly record max temps
    wmin_temps = [] #list of yearly record min temps
    wunique_year = [] #list of unique years
        
    wrecords = []  #all records from the parsed file
    wmaxt = [] # temporarily stores all max temps for a year
    wmint = [] # temporarily stores all min temps for a year
    year = "" # a string for checking year changes

    #open the file, read it into wrecords, close the file
    with open(infile, mode='r') as file:
        
        file.readline()

        for rec in file:
            wrecords.append(rec.split())

    #assign to the first year
    year = wrecords[0][2][0:4]

    for row in wrecords:
        #extract the date
        wdates.append(row[2])
        #extract the temperature as a float
        wtemperatures.append(float(row[3]))
        #extract only the year as a float
        wyear.append(float(row[2][0:4]))
        
        #make a list of unique years
        if float(row[2][0:4]) not in wunique_year:
            wunique_year.append(float(row[2][0:4]))
        
        #When the year changes or the records end, calculate year max and min temps, reset temps for next year
        if year != row[2][0:4] or len(wyear) == len(wrecords):
            year = row[2][0:4]
            wmax_temps.append(max(wmaxt))
            wmin_temps.append(min(wmint))
            wmaxt = []
            wmint = []
        
        #add to the list of max and min temps for the year
        if float(row[17]) < 200.00:
            wmaxt.append(float(row[17]))
        if float(row[18]) < 200.00:
            wmint.append(float(row[18]))
        
    return wdates, wtemperatures, wyear, wmax_temps, wmin_temps, wunique_year


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

    #For each month calculate the mean and the standard deviation
    while(month <= 12):
        sumt = 0.0
        month_temps = []
        
        #create string to check for compatible months
        if(month < 10):
            check_month = "0" + str(month)
        else:
            check_month = str(month)
        
        #get the sum of all temps for the month and a list of those temps
        for index, date in enumerate(wdates):
            if(date[4:6] == check_month):
                
                sumt = sumt + wtemp[index]
                month_temps.append(wtemp[index])
        
        #add the month's mean and standard deviation
        means.append(sumt / len(month_temps))
        std_dev.append(np.std(month_temps))
        
        #go to next month
        month = month + 1

    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1. This will show the temperatures of the year, and a bar graph
    of average monthly temperatures with the standard deviation
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
    plt.ylabel("Daily Temperature, F")
    plt.xlabel("Year")
    plt.xlim([1970, 2015])
    plt.ylim([-20, 100])

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Average Temperature, F")
    plt.xlabel("Month")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.yticks(np.arange(0, 100, step=10))
    plt.show()      # display plot


def plot_data_task2(wyear, wmax_temps, wmin_temps):
    """
    Create plot for Task 2. This plot will show the yearly max and min temperatures recorded
    :param: wyear: list with year (in decimal)
    :param: wmax_temps: list with max temps per year (in decimal)
    :param: wmin_temps: list with min temps per year (in decimal) 
    """
    plt.title("Record Yearly Temperatures, Ogden")#create the plot
    plt.xlabel("Year")
    plt.ylabel("Temperature, F")
    plt.plot(wyear, wmax_temps, "ob", label="Maximum Temp")
    plt.plot(wyear, wmin_temps, "oy", label ="Minimum Temp")
    plt.legend()
    plt.show()#show the plot


def main(infile):
    """
    Takes the infile of weather data, parses it, and plots it
    :param: infile: file of weather data
    """
    weather_data = infile    # take data file as input parameter to file
    wdates, wtemperatures, wyear, wmax_temps, wmin_temps, wunique_year = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    
    plot_data_task1(wyear, wtemperatures, month_mean, month_std)
    
    plot_data_task2(wunique_year, wmax_temps, wmin_temps)

if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = sys.argv[0]
    main("data/CDO6674605799016.txt")
    exit(0)
