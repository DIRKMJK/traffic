from pathlib import Path
from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

DOMAIN = "https://www.schiphol.nl"
URL = DOMAIN + "/nl/schiphol-group/pagina/verkeer-en-vervoer-cijfers/"
LABEL = 'Maandelijkse Verkeer & Vervoer cijfers 1992 - heden'
TOPICS = ['flights', 'pax_1', 'pax_2', 'pax_3']


def is_correct_link(element):
    """Identify correct download link"""
    payload = element.get('data-analytics-payload')
    if not payload:
        return False
    return LABEL in payload


def download_data():
    """Download Schiphol Airport traffic data excel file."""
    html = requests.get(URL).text
    soup = bs(html, 'lxml')
    for element in [e for e in soup.find_all('a') if is_correct_link(e)]:
        url = DOMAIN + element.get('href')
        break
    r = requests.get(url)
    return r.content


def convert_date(date):
    """Convert date to Y-m"""
    if date.endswith('Total'):
        return date[:4]
    date = datetime.strptime(date, '%Y%B')
    return datetime.strftime(date, '%Y-%m')


def clean_data(path='../data/data.xlsx', subset=None):
    """Read Schiphol traffic data from excel and clean data

    :param path: path where excel file is stored
    :param subset: if 'months' return only montly data; if 'years'
        return only yearly data

    """

    df = pd.read_excel(path, skiprows=8)
    df = df[pd.notnull(df.Month)]
    df = df.rename(columns={
        df.columns[19]: 'Cargo (tonnes)',
        df.columns[20]: 'Mail (tonnes)'
    })
    df['Year'] = df.Year.replace(to_replace=None, method='ffill')
    df.index = df.Year.map(str) + df.Month
    df.index = df.index.map(lambda x: convert_date(x))
    drop = [c for c in df.columns if c.startswith('Unnamed')]
    df = df.drop(drop, axis=1)
    for i, topic in enumerate(TOPICS):
        cols = 3
        if i == 3:
            cols = 4
        start = 2 + i * 3
        for col_index in range(start, start + cols):
            colname = df.columns[col_index]
            df = df.rename(columns={
                colname: f'{topic}_{colname}'.split('.')[0]
            })
    if subset == 'months':
        df = df[df.Month != 'Total']
    elif subset == 'years':
        df = df[df.Month == 'Total']
    return df


def create_index(series):
    """Convert a series into a list of index values starting at 100"""
    return [100 * value / series[0] for value in series]


def calc_growth_perc(series, i, lapse=12):
    """Create growth percentage relative to t-lapse

    :param i: index of value to calculate percentage for
    :param lapse: 12 to compare to same month of previous year,
        1 to compare to previous year

    """

    if i < lapse:
        return None
    return 100 * (series[i] - series[i - lapse]) / series[i - lapse]

def calculate_wlu(df, pax='pax_1_Total*', cargo='Cargo (tonnes)'):
    """Calculate work load units
    :param pax: column with passenger data to use
    :param cargo: column with cargo data to use
    """
    return df[pax] + 10 * df[cargo]
