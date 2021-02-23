# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Welling Wang 
# Collaborators (discussion):Boe Wang
# Time:5hours

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    models=[]
    for d in degs:
        model = pylab.polyfit(x, y, d)
        models.append(model)
    return models

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    error=((estimated-y)**2).sum()
    meanError=error/len(y)
    return 1-(meanError/pylab.var(y))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    pylab.plot(x, y, 'bo', label = 'Data',alpha=0.7)
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = r_squared(y, estYVals)
        SE_slope=se_over_slope(x, y, estYVals, models[i])
        pylab.plot(x, estYVals, "r-", 
                   label = 'Fit of degree '\
                   + str(degs[i])\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.xlabel('years')
    pylab.ylabel('degrees Celsius')
    pylab.legend(loc = 'best')
    pylab.title(title+"\n"+" SE/slope= "+str(SE_slope))
##    pylab.show()
    pylab.savefig(title)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    temps=[]
    for year in years:
        avg=[]
        for city in multi_cities:
            y=climate.get_yearly_temp(city,year)
            avg.append(y.sum()/len(y))
        temps.append(sum(avg)/len(avg))
    return pylab.array(temps)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    mv_avg=[]
    for i in range(len(y)):
        if i<window_length:
            mv=sum(y[:i+1])/len(y[:i+1])
            mv_avg.append(mv)
        else:
            mv=sum(y[i-window_length+1:i+1])/window_length
            mv_avg.append(mv)
    return pylab.array(mv_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    mean_error=((y-estimated)**2).sum()/len(y)
    return mean_error**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    std_devs=[]
    for year in years:
        avg=[]
        for city in multi_cities:
            y=climate.get_yearly_temp(city,year)
            avg.append(y)
        std_devs.append(pylab.std(sum(avg)/len(multi_cities)))
    return pylab.array(std_devs)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    pylab.plot(x, y, 'bo', label = 'Data',alpha=0.7)
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = r_squared(y, estYVals)
        RMSE=rmse( y, estYVals)
        pylab.plot(x, estYVals,
                   label = 'Fit of degree '\
                   + str(degs[i])\
                   + ', R2 = ' + str(round(error, 5))+" RMSE= "+str(round(RMSE,5)))
    pylab.xlabel('years')
    pylab.ylabel('degrees Celsius')
    pylab.legend(loc = 'best')
    pylab.title(title+"\n")
##    pylab.show()
    pylab.savefig(title)

if __name__ == '__main__':
##
##    # Part A.4
##    # TODO: replace this line with your code
##    
##    data=Climate("data.csv")
##    years,temps=[],[]
##    for year in TRAINING_INTERVAL:
##        temp=data.get_daily_temp('NEW YORK', 1, 10, year)
##        years.append(year)
##        temps.append(temp)
##    x=pylab.array(years)
##    y=pylab.array(temps)
##    degs=[1]
##    title="New York daily average"
##    models=generate_models(x, y, degs)
##    evaluate_models_on_training(x, y, models)
##
##    
##    data=Climate("data.csv")
##    years,temps=[],[]
##    for year in TRAINING_INTERVAL:
##        y=data.get_yearly_temp('NEW YORK',year)
##        avg=y.sum()/len(y)
##        years.append(year)
##        temps.append(avg)
##    x=pylab.array(years)
##    y=pylab.array(temps)
##    degs=[1]
##    title="New York yearly average"
##    models=generate_models(x, y, degs)
##    evaluate_models_on_training(x, y, models)
##    #temps data below:
##    """[12.013150684931505, 11.085479452054795, 11.564931506849318, 11.943989071038251,
##    11.325890410958905, 11.776164383561644, 10.36109589041096, 11.413661202185795,
##    12.225753424657533, 12.166301369863016, 12.807123287671233, 12.465300546448088,
##    12.704657534246577, 12.408356164383562, 12.594931506849317, 11.243852459016393,
##    11.35095890410959, 11.904109589041095, 12.015068493150684, 11.99931693989071,
##    12.472602739726028, 12.281643835616437, 13.20082191780822, 12.91571038251366,
##    12.57931506849315, 12.361917808219179, 12.238356164383562, 11.899726775956287,
##    11.810136986301371, 13.189041095890412, 13.507534246575343, 11.773770491803278,
##    12.415753424657535, 12.320273972602742, 12.76931506849315, 11.553005464480874,
##    12.194109589041098, 13.372328767123287, 12.926986301369864, 11.68415300546448,
##    12.792876712328766, 12.91150684931507, 11.56972602739726, 12.116393442622952,
##    12.457123287671234, 13.238356164383559,
##    12.462465753424658, 12.705464480874314, 12.184657534246574]"""
##
##
##    # Part B
##    # TODO: replace this line with your code
##    climate=Climate("data.csv")
##    years=[]
##    for year in TRAINING_INTERVAL:
##         years.append(year)
##    x=pylab.array(years)
##    multi_cities=CITIES
##    y=gen_cities_avg(climate, multi_cities, years)
##    degs=[1]
##    title="national yearly average"
##    models=generate_models(x, y, degs)
##    evaluate_models_on_training(x, y, models)
##
##        
##    # Part C
##    # TODO: replace this line with your code
##    climate=Climate("data.csv")
##    years=[]
##    for year in TRAINING_INTERVAL:
##         years.append(year)
##    x=pylab.array(years)
##    multi_cities=CITIES
##    get_y=gen_cities_avg(climate, multi_cities, years)
##    y=moving_average(get_y,5)
##    degs=[1]
##    title="national yearly moving average"
##    models=generate_models(x, y, degs)
##    evaluate_models_on_training(x, y, models)

##    # Part D.2
##    # TODO: replace this line with your code
##    climate=Climate("data.csv")
##    years1=[]
##    for year in TRAINING_INTERVAL:
##         years1.append(year)
##    x1=pylab.array(years1)
##    multi_cities=CITIES
##    get_y=gen_cities_avg(climate, multi_cities, years1)
##    y1=moving_average(get_y,5)
##    degs=[1,2,20]
##    models=generate_models(x1, y1, degs)
##    title="more national yearly moving average"
##    evaluate_models_on_training(x1, y1, models)
##    
##    years2=[]
##    for year in TESTING_INTERVAL:
##         years2.append(year)
##    x2=pylab.array(years2)
##    multi_cities=CITIES
##    get_y=gen_cities_avg(climate, multi_cities, years2)
##    y2=moving_average(get_y,5)
##    title="predict national yearly moving average"
##    evaluate_models_on_testing(x2, y2, models)
##
##    # Part E
##    # TODO: replace this line with your code
##    climate=Climate("data.csv")
##    years=[]
##    for year in TRAINING_INTERVAL:
##         years.append(year)
##    x=pylab.array(years)
##    multi_cities=CITIES
##    get_y=gen_std_devs(climate, multi_cities, years)
##    y=moving_average(get_y,5)
##    degs=[1]
##    title="national yearly average moving std"
##    models=generate_models(x, y, degs)
##    evaluate_models_on_training(x, y, models)
