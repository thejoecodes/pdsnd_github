import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']

MONTHS = ['all','january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data from Motivate, a bike sharing company!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in CITIES:
        #Prompts the user to enter the city name
        city = input('\nWhich city do you want to explore Chicago, New York City or Washington? \n> ').lower()
        if city in CITIES:
            break
        else:
            #Gives the user a chance to re-enter the city name incase of an invalid input
            print("\nInvalid city name, we only have data for chicago, new york city or washington. Please input any of the three\n")

    #get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in MONTHS:
        month = input("\nWhich month's data are you interested in? (E.g. Input 'all' for all months or select a month between january to june.\n").lower()
        #Breaks the flow if the correct month name is entered by the user
        if month.lower() in MONTHS:
            break
        else:
            #Gives the user another chance to re-enter the month's name on an invalid entry
            print("Invalid month name, Please input either 'all' to apply no month filter or select a month between january to june.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.lower() not in DAYS:
        #prompts and gets the user input for the day of week name
        day = input('\n Which day\'s data are you interested in? Input all or any day from sunday to saturday\n ').lower()
        if day.lower() in DAYS:
            break
        else:
            #Request the user to re-enter the day of the week in case of an invalid entry
            print('\n Invalid input! Please input all or a day from sunday to saturday.\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month)
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print('\n The most common month from your input is :', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print('\n The most common day from your input is :', common_day)

    # display the most common start hour
    common_start_hour = df['hour'].value_counts().idxmax()
    print('\n The most common day from your input is :', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("\n The most commonly used start station from your input is: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("\n The most commonly used end station from from your input is: " + common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].value_counts().idxmax()
    print("\n The most commonly used start station and end station : {}, {}"\
          .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time :", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\n Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    #prints out the total number of user counts iteratively
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    
    print()
    
    if 'Gender' in df.columns:
        user_stats_gender(df)
        
    if 'Birth Year' in df.columns:
        user_stats_birth(df)
        
    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)  
    
       
def user_stats_gender(df):
    """To display the statistical analysis based on gender."""
    # Display counts of gender
    print("\n Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    
    # prints out the total numbers of genders iteratively 
    for index,gender_count   in enumerate(gender_counts):
        print("\n  {}: {}".format(gender_counts.index[index], gender_count))
    
    print()
       
def user_stats_birth(df):
    """To display the statistical analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # most common birth year
    common_birth_year = birth_year.mode()[0]
    print("The most common birth year:", common_birth_year)
    # most recent birth year
    recent_birth_year = birth_year.max()
    print("The most recent birth year:", recent_birth_year)
    # most earliest birth year
    earliest_birth_year = birth_year.min()
    print("The most earliest birth year:", earliest_birth_year)
   
def trip_stats(df, city):
    """Displays other important statistics on bikeshare users."""
    print('\n Calculating Other Dataset Stats...\n')
    
    # the number of missing values in the entire dataset
    number_of_missing_values = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city, number_of_missing_values))

    # the number of missing values in the User Type column
    number_of_nonzero = np.count_nonzero(df['User Type'].isnull())
    print("The number of missing values in the \'User Type\' column: {}".format(number_of_missing_values))
    
def display_data(df):
    """To display raw bikeshare data."""
    print(df.head())
    next = 0
    while True:
        raw_data = input('\n Would you like to view next five row of raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_stats(df, city)
        
        while True:
            raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break
            display_data(df)
            break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
