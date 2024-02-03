import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
from multiprocessing import Pool


# Get the Results for the last 10 years
for year, url in {
    2023: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2023",
    2022: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2022",
    2021: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2021",
    2020: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2020",
    2019: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2019",
    2018: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2018",
    2017: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2017",
    2016: "https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_2016",
}.items():
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find(lambda tag: tag.name == "span" and "Full list" in tag.text)
    section_or_div = header.find_parent("h2").find_next_sibling(
        "table", class_="wikitable"
    )
    table_html = str(section_or_div)
    table_io = StringIO(table_html)
    df_list = pd.read_html(table_io)

    df = df_list[0]
    df.columns = ["rank"] + df.columns[1:].tolist()
    df.set_index("rank", inplace=True)

    df.to_csv(f"data/{year}_results.csv")


def get_plays_for_year(year):
    start = datetime.strptime(f"{year}-01-01T01:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    end = datetime.strptime(f"{year+1}-01-01T01:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")

    filename = f"data/{year}_plays.json"

    next_start_time = start

    while next_start_time < end:
        url = f"http://music.abcradio.net.au/api/v1/plays/search.json?station=triplej&from={next_start_time.strftime('%Y-%m-%dT%H:%M:%S')}&order=asc"

        played = requests.get(url).json()["items"]
        last_song_time_string = played[-1]["played_time"]
        next_start_time = datetime.strptime(
            last_song_time_string, "%Y-%m-%dT%H:%M:%S%z"
        ) + timedelta(seconds=1)
        print(next_start_time)

        with open(filename, "a+") as f:
            json_str = "\n".join([json.dumps(i) for i in played])
            f.write(json_str)


pool = Pool()
pool.map(get_plays_for_year, range(2016, 2024))


def process_object(string):
    try:
        dic = json.loads(string)
        out = {
            "timestamp": dic["played_time"],
            "title": dic["recording"]["title"],
            "artist": dic["recording"]["artists"][0]["name"],
            "aus": dic["recording"]["artists"][0]["is_australian"],
            "duration": dic["recording"]["duration"],
            "album_title": dic["recording"]["releases"][0]["title"],
            "release_year": dic["recording"]["releases"][0]["release_year"],
        }
        return out
    except:
        return None


for year in range(2016, 2024):
    input_filename = f"data/{year}_plays.json"
    output_filename = f"data/{year}_filtered.json"

    with open(input_filename, "r") as input_file:  # Add the missing square brackets
        uncleaned_data = input_file.read()
        data_list = []
        for line in uncleaned_data.split("\n"):
            for entry in line.split("}{"):
                string = ""
                if not entry.startswith("{"):
                    string = "{" + entry
                else:
                    string += entry

                if not string.endswith("}"):
                    if string.endswith(","):
                        string = string[:-1]
                    else:
                        string += "}"

                if not string.endswith("}"):
                    string += "}"

                data_list.append(string)

    filtered_data = map(process_object, data_list)
    filtered_data = [x for x in filtered_data if x is not None]

    with open(output_filename, "w") as output_file:
        output_file.write(json.dumps(filtered_data))
