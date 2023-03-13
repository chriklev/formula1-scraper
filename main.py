import bs4 as bs
from urllib.request import urlopen
import pandas as pd
import re


def get_race_urls(year):
    source = urlopen(
        f"https://www.formula1.com/en/results.html/{year}/races.html").read()
    soup = bs.BeautifulSoup(source, 'html.parser')

    race_urls = set()

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if year in url and '/race-result.html' in url:
            race_urls.add(url)
    return race_urls


def seasons_results(year, homepage='https://www.formula1.com/'):
    year = str(year)
    race_urls = get_race_urls(year)

    season_results_df = pd.DataFrame()
    for race_url in race_urls:
        race_name = race_url.split('/')[6]

        results_page = urlopen(homepage + race_url).read()
        race_results = bs.BeautifulSoup(results_page, 'html.parser')

        tables = race_results.find_all('table')
        if len(tables) > 0:
            table = tables[0]
        else:
            continue
        df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
        df.drop(["Unnamed: 0", "Unnamed: 8"], axis=1, inplace=True)
        df.set_index('No', inplace=True)
        df['Race Year'] = year
        df['Race Name'] = race_name

        season_results_df = pd.concat([season_results_df, df])

    return (season_results_df)


def all_results(from_year, to_year):
    all_results = pd.DataFrame()
    for year in range(from_year, to_year+1):
        print(year)
        df = seasons_results(year)
        all_results = pd.concat([all_results, df])
    return all_results


if __name__ == '__main__':
    df = all_results(1980, 2023)
    df.to_csv('1980_to_2023_results.csv')
