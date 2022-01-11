"""
Web Scraping Script (Twitter)

Given the USERNAME of said university, this program leverages Twint (twitter web scraping software)
to retrive all tweets published (and possibly deleted) from the given DATE until the present time
that the program was run.

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
import twint

# date of inital covid-19 outbreak
DATE = '2020-03-20'

# initial configuration
c = twint.Config()
c.Since = DATE
c.Retweets = True
c.Count = True
c.Limit = 5000
c.Store_csv = True
c.Hide_output = True


def collect_tweets(username: str) -> str:
    """
    Return the filename of stored tweets from the given username. Tweets are scraped
    using twint library by a username search. File stored as a .csv file.
    """

    # configuration
    c.Username = username
    c.Output = './Datasets/Tweets_Dataset_' + username + '.csv'

    # running search
    twint.run.Search(c)

    return 'Tweets_Dataset_' + username + '.csv'
