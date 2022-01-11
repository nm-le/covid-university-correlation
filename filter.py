"""
Filters Ontario COVID data and all universities' tweets to useful data.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of evaluators
of CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021:
    Kurtis Law
    Shaan Purewal
    Hyun Bin Antonio Kim
    Minh Ngoc Le

"""
import csv
import datetime
from math import sqrt, sin, asin, radians

INITIAL_DATE = datetime.date(2020, 3, 20)

KEYWORDS_LIST = {
    'mask': 4,
    'distancing': 6,
    'vaccine': 7,
    'vaccination': 7,
    'online school': 8,
    'on-campus': 8,
    'on campus': 8,
    'safe': 4,
    'screening': 3,
    'measure': 2,
    'outbreak': 5,
    'closed': 8,
    'gathering': 6,
    'response': 4,
    'Social distancing': 5,
    'social distancing': 5,
    'UCheck': 2,
    'government': 1,
    'test': 3,
    'cover': 2,
    'precautions': 6,
    'challenges': 1,
    'obstacles': 1,
    'quarantine': 8,
    'tracing': 2,
    'limit': 5,
    'public': 1,
    'spread': 1,
    'stay': 1
}

RADIUS = 5


class University:
    """
    Defines all neccessary attributes, getters for each university.

    Representation Invariants:
        - self.display_name != ''
        - 41.66 <= self.location[0] <= 56.86
        - -95.16 <= self.location[1] <= -74.34
        - self.tweet_csv_path != ''

    """
    tweet_csv_path: str
    display_name: str
    impact_dic: dict[int, int]
    covid_dic: dict[int, int]
    location: tuple[float, float]

    def __init__(self, display_name: str, impact_dic: dict[int, int], covid_dic: dict[int, int], 
                 location: tuple[float, float], tweet_csv_path: str) -> None:
        self.display_name = display_name
        self.impact_dic = impact_dic
        self.covid_dic = covid_dic
        self.location = location
        self.tweet_csv_path = tweet_csv_path


# Initializing all the universities
brocku = University(display_name='Brock University',
                    impact_dic={},
                    covid_dic={},
                    location=(43.117573, -79.247692),
                    tweet_csv_path='Datasets/Tweets_Dataset_BrockUniversity.csv')

queensu = University(display_name='Queens\' University',
                     impact_dic={},
                     covid_dic={},
                     location=(44.224997, -76.495099),
                     tweet_csv_path='Datasets/Tweets_Dataset_queensu.csv')

uoft = University(display_name='University of Toronto',
                  impact_dic={},
                  covid_dic={},
                  location=(43.664486, -79.399689),
                  tweet_csv_path='Datasets/Tweets_Dataset_UofT.csv')

uw = University(display_name='University of Waterloo',
                impact_dic={},
                covid_dic={},
                location=(43.467998128, -80.537331184),
                tweet_csv_path='Datasets/Tweets_Dataset_UWaterloo.csv')

westernu = University(display_name='Western University',
                      impact_dic={},
                      covid_dic={},
                      location=(43.009953, -81.273613),
                      tweet_csv_path='Datasets/Tweets_Dataset_WesternU.csv')


uni_list = [brocku, queensu, uoft, uw, westernu]

###############################################################################
# Part 1 - Creating impact_dic from filtering twitter
###############################################################################


def creating_impact_dic(uni: University) -> dict:
    """Creates an impact dic for a singular university

        Processes all universities' tweets to only retain useful data. We do this by:
         1. Keeping only columns 'tweet', 'created_at' and 'name'
         2. Removing all tweets that do not mention 'COVID' or 'covid'
         3. Only keeping tweets that have an impact score of at least 1
         4. Converting the date from a YYYY-MM-DD format to an integer representing days
         since March 20, 2020
    """
    with open(uni.tweet_csv_path, encoding="utf-8") as f:
        # Reading the csv file
        csv_reader = csv.reader(f)

        # Creating impact_dic, which contains maps all impact scores to its date
        impact_dic = {}
        for row in csv_reader:
            if row[0] != 'id':
                # Implementing step 1 of docstring
                tweet = row[10]
                hashtag = row[18]

                # Implementing step 2 of docstring
                if 'COVID' in tweet or 'covid' in tweet:
                    date = row[3]

                    # Implementing step 3 of docstring
                    impact_score = calculate_impact_score(tweet, hashtag)

                    # Converting string to an integer representing days since March 20, 2020
                    dt_object = datetime.datetime.strptime(
                        date, "%Y-%m-%d").date()

                    delta = dt_object - INITIAL_DATE

                    # Appending our useful values
                    if delta.days not in impact_dic:
                        impact_dic[delta.days] = impact_score
                    else:
                        impact_dic[delta.days] += impact_score

        # Converting impact_dic into a dictionary that maps week to its cumulative impact scores
        dates = list(impact_dic)
        dates.reverse()
        cases = list(impact_dic.values())
        cases.reverse()

        week_dic = {}
        week_cumulative = 0
        week_number = 0
        for date, case in zip(dates, cases):
            if date % 7 == 0 and date != 0:
                week_cumulative += case
                week_dic[week_number] = week_cumulative
                week_number += 1
                week_cumulative = 0
            else:
                week_cumulative += case
        return week_dic


def calculate_impact_score(tweet: str, hashtag: str) -> int:
    """
    Returns impact score for each tweet based on keyword dictionary.

    >>> calculate_impact_score('Please stay safe during COVID-19 epidemic!', '#COVID19')
    5
    >>> calculate_impact_score('During COVID-19 we where able to raise funds for the homeless', '#UOFT')
    0
    """
    cumulative_impact_score = 0

    # If a key from KEYWORDS_LIST is present in a tweet or hashtag, then the key's impact score
    # is summed to the day's cumulative_impact_score
    for keyword in KEYWORDS_LIST:
        if keyword in tweet:
            cumulative_impact_score += KEYWORDS_LIST[keyword]

    if hashtag in KEYWORDS_LIST:
        cumulative_impact_score += KEYWORDS_LIST[hashtag]

    return cumulative_impact_score


###############################################################################
# Part 2 - Creating covid_dic from filtering Ontario COVID data
###############################################################################

def creating_covid_dic(uni: University) -> dict:
    """Returns a dictionary mapping the amount of COVID-cases to a day."""
    with open('Datasets/Ontario_Covid_Dataset.csv', encoding="utf-8") as covid_data:
        csv_reader = csv.reader(covid_data)

        dates = []
        covid_cases = []

        for row in csv_reader:
            date = row[1]
            if date != 'Accurate_Episode_Date':  # to forcefully ignore first line
                case_latitude = row[16]
                case_longitude = row[17]

                # convert string to an integer representing days since march 20, 2020
                dt_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                delta = dt_object - INITIAL_DATE

                # Starts counting covid cases since March 20th, 2020
                if delta.days >= 0:
                    uni_latitude = uni.location[0]
                    uni_longitude = uni.location[1]

                    # If university is within range, add the values to that
                    # specific university's lists.
                    if within_range(
                            float(case_latitude),
                            float(case_longitude),
                            uni_latitude,
                            uni_longitude,
                            RADIUS):
                        if delta.days not in dates:
                            dates.append(delta.days)
                            covid_cases.append(1)
                        else:
                            index = dates.index(delta.days)
                            covid_cases[index] += 1

        # return file in dictionary format for convenient use in visualization
        covid_dic = {date: covid_cases for date,
                     covid_cases in zip(dates, covid_cases)}

        # Converting covid_dic into a dictionary that maps week to its
        # cumulative number of COVID cases
        dates = list(covid_dic)
        cases = list(covid_dic.values())

        week_dic = {}
        week_cumulative = 0
        week_number = 0
        for date, case in zip(dates, cases):
            if date % 7 == 0 and date != 0:
                week_cumulative += case
                week_dic[week_number] = week_cumulative
                week_number += 1
                week_cumulative = 0
            else:
                week_cumulative += case
        return week_dic


def within_range(lat1: float, long1: float, lat2: float, long2: float, range: float) -> bool:
    """Returns whether lat1 and long2 is within range km with lat2 and long2."""
    return haversine(lat1, long1, lat2, long2) <= range


def haversine(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """Determines the distance between two coordinates.
    We take r as the average radius of the Earth: 6378 km.

    >>> import math
    >>> bahen = (43.65983570963418, -79.39694225927128)
    >>> margad = (43.668387110900944, -79.39244320160002)
    >>> output = haversine(bahen[0], bahen[1], margad[0], margad[1])
    >>> math.isclose(output, 1.02, abs_tol=1e-2)
    True
    """
    # change degree values of latitude and longitude into radians
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    long1 = radians(long1)
    long2 = radians(long2)

    r = 6378  # the average distance from earth's core to the surface

    # Calculate distance between two locations
    d = 2 * r * asin(
        sqrt(
            (sin((lat2 - lat1) / 2)) ** 2
            + (1 - ((sin(lat2 - lat1) / 2) ** 2)
            - ((sin((lat2 + lat1) / 2)) ** 2))
            * (sin(long2 - long1) / 2) ** 2
        )
    )
    return d


###############################################################################
# Part 3 - Completing each universities' class representation
###############################################################################

def compile_universities() -> None:
    """Complete function calls for each university. """
    print('~ Generating data can take up to a minute. Thanks for being patient.')
    for index, uni in enumerate(uni_list):
        uni.impact_dic = creating_impact_dic(uni)
        uni.covid_dic = creating_covid_dic(uni)
        print(
            f'~ Data for {uni.display_name} generated. {index + 1} out of {len(uni_list)} done!')
    print('! Classes created for all universities.')


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
