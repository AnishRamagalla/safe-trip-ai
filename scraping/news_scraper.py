import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_us_travel_advisories():
    url = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    alerts = []
    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            country = cells[0].text.strip()
            level = cells[1].text.strip()
            alerts.append({"country": country, "threat_level": level})

    df = pd.DataFrame(alerts)
    df["threat_numeric"] = df["threat_level"].str.extract(r'(\d)').astype(int)
    return df
