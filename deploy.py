import requests
from bs4 import BeautifulSoup
import datetime
import os
import time

def main():
    url = "https://www.falmouthharbour.co.uk/wind-speed/"
    r = requests.get(url).content

    soup = BeautifulSoup(r, 'html.parser')

    row = soup.find('table').tbody.tr

    td = row.find_all('td')

    if len(td) == 8:
        # Complete table response
        
        #Create string starting with current UTC Date for csv parsing
        s = f"{datetime.datetime.utcnow().date()},"
        for element in td:
            s += f"{element.text},"
        
        # Strip final trailing comma
        s = s.rstrip(",")

        # Path to current file
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Context manager to write out
        with open(os.path.join(dir_path, "wind_data.csv"), 'a') as f:
            f.write(f"{s}\n")


    else:
        # Incomplete table response
        # Strategy is to sleep for ten seconds then retry
        # range(60) bc 600 seconds is 10 mins, and table updates every 10 mins
        for _ in range(60):
            time.sleep(10)
            main()


main()