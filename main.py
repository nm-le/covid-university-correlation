"""
Main function.

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
import Twint_Scrape
import filter
import visualisation
import setup
from tqdm import tqdm
import os

TWITTER_HANDLES = {
    'University of Toronto': 'UofT',
    'Western University': 'WesternU',
    'University of Waterloo': 'UWaterloo',
    'Queens University': 'queensu',
    'Brock University': 'BrockUniversity'
}


def scrape_datasets(handles: dict[str, str]) -> None:
    """
    Create a .csv file dataset of tweets from each university within 'handles',
    given the twitter username of said university. Return None.
    """
    for i in tqdm(range(len(handles.keys())),
                  desc="Loading…",
                  ascii=False, ncols=75):
        uni = list(handles.keys())[i]
        filename = Twint_Scrape.collect_tweets(handles[uni])
        print(f'~ {uni} dataset has been stored in the file {filename}, '
              f'within the Datasets directory')


if __name__ == "__main__":
    # setup configuration files and Datasets
    if not os.path.exists('Datasets'):
        os.mkdir('Datasets')
    setup.start()

    # scrape for tweets
    
    scrape_datasets(TWITTER_HANDLES)
    print('~ All requested university twitter accounts have been scraped for tweets')

    # # filter data
    filter.compile_universities()

    # # visualize data
    if not os.path.exists('output'):
        os.mkdir('output')
    visualisation.plot_impacts()
    visualisation.plot_covid()
    print('Successfully exported all graphs under "./output"')
