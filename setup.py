"""
Run this setup file to ensure twint is properly configured for tweets scraping
without any limitations. The purpose of this file is to navigate the configuration files
of your twint location and alter specific lines, known to bottleneck twint. In addition,
'setup' of this program will ensure no datafiles exist within the Datasets directory to
ensure old data isn't mixed with newly sourced data. If needed Ontario Dataset will be
downloaded.


Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of evaluators
of CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021:
    Law Chak Huen Kurtis
    Shaan Purewal
    Hyun Bin Antonio Kim
    Minh Ngoc Le
"""
import platform
import site
import os
from pathlib import Path

# corrected user-agent profile for each respective hardware type know to trigger GUEST HTML ERROR
import requests

token_config = {
    'arm64': '(Macintosh; Intel Mac OS X 12.0; rv:78.0)',
    'x86_64': '(Macintosh; Intel Mac OS X 12.0; rv:78.0)',
    'AMD64': '(Windows NT 10.0; Win64; x64; rv:78.0)'
}


def start() -> None:
    """
    Edit configuration file to ensure no errors/limitations are called during data-scraping. Empty
    Datasets directory to ensure only newly sourced data is stored. Return None.
    """

    # identify hardware type
    machine = platform.uname().machine

    # configure token.py file (if needed)
    if machine in token_config:
        configure_token(machine)

    # configure url.py file
    configure_url()

    # empty Datasets directory
    clear_data_directory()

    # Check Covid-19 data
    download_covid_data()

    # print success notification
    print('~ Successfully setup twint for use!')


def configure_token(machine: str) -> None:
    """
    Locate and edit token.py configuration file of the installed twint package. Purpose
    is to edit (line  20 of) the token.py file to prevent GUEST HTML TOKEN ERROR. Given machine
    type, correct configuration of user-agent. Return None.
    """

    # locate token.py file
    token = Path(site.getsitepackages()[-1]) / 'twint' / 'token.py'

    # read file
    with open(token, 'r') as file:
        data = file.readlines()

    # edit specified line
    data[20] = data[20].replace('(Windows NT 10.0; Win64; x64; rv:78.0)', token_config[machine])

    # write new data to file
    with open(token, 'w') as file:
        file.writelines(data)

    # print success notification
    print('~ Agent User Corrected!')


def configure_url() -> None:
    """
    Locate and edit url.py/token.py configuration file of the installed twint package. Purpose
    is to uncomment a line of code to aid in superseding Twitter's web-scraping bottlenecks. Aswell
    as editing (line  20 of) the token.py file to prevent GUEST HTML TOKEN ERROR.
    """

    # locate url.py file
    url = Path(site.getsitepackages()[-1]) / 'twint' / 'url.py'

    # read file
    with open(url, 'r') as file:
        data = file.readlines()

    # edit specified line
    data[91] = data[91].replace('#', '')

    # write new data to file
    with open(url, 'w') as file:
        file.writelines(data)

    # print success notification
    print('~ Query Search Corrected!')


def clear_data_directory() -> None:
    """
    Locate Datasets directory and  delete any existent files. Return None.
    """

    files = os.listdir('Datasets')

    for file in files:
        if file != '.DS_Store':
            os.remove(Path('Datasets') / file)

    # print success notification
    print('~ Datasets Cleared!')


def download_covid_data() -> None:
    """
    If ontario Covid-19 data not found download data from the Ontario
    Data Catalogue. Return None.
    """

    dir = 'Datasets'
    files = os.listdir(dir)
    url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27' \
          '/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'

    if 'Ontario_Covid_Dataset.csv' not in files:
        print('~ Downloading Covid-19 Dataset')

        data = requests.get(url, allow_redirects=True)
        open(Path(dir) / 'Ontario_Covid_Dataset.csv', 'wb').write(data.content)

        print('~ Covid-19 Dataset Downloaded!')
    else:
        print('~ Covid-19 Dataset Detected!')
