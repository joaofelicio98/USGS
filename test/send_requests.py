import requests
from random import randrange
import random
from datetime import timedelta
import datetime
from concurrent.futures import ThreadPoolExecutor

base_url = input("base url: ")

def create_rand_urls(base_url):
    urls = []
    startdate = datetime.date(2013, 1, 1)
    enddate = datetime.date(2022,1,1)
    time_between_dates = enddate - startdate
    days_between_dates = time_between_dates.days
    for _ in range(500):
        random_number_of_days = random.randrange(days_between_dates)
        starttime = startdate + timedelta(days=random_number_of_days)
        endtime = starttime + timedelta(days=20)
        url = base_url + f"/first?starttime={starttime}&endtime={endtime}"
        urls.append(url)
    return urls


def fetch(session, url):
    with session.get(url) as response:
        #print(response)
        if response.status_code != 200:
            print(response)

def main():
    urls = create_rand_urls(base_url)
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            executor.map(fetch, [session]*500, urls)
            executor.shutdown(wait=True)

if __name__ == "__main__":
    main()
