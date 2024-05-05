import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# key is months value is range of days
calender = {1: range(1, 32), 2: range(1, 29), 3: range(1, 32), 4: range(1, 31), 5: range(1, 32), 6: range(1, 31),
            7: range(1, 32), 8: range(1, 32), 9: range(1, 31), 10: range(1, 32), 11: range(1, 31), 12: range(1, 32)}
YEAR = 2018

first_winners = []
main_df = pd.DataFrame()

print("Generating xlsx....")
for month, days in calender.items():
    # Iterate through the possible days of the month
    for day in days:
        URL = f"https://www.check4d.org/past-results/{YEAR}-{month}-{day}#section-sg"

        page = requests.get(URL)
        numbers = []
        soup = BeautifulSoup(page.content, "html.parser")
        # get first number

        first_winner = soup.find(id="sp1")
        # Check if valid 4d for that day
        if not first_winner:
            continue
        else:
            first_winners.append(first_winner.text)
            numbers.append(first_winner.text)
        numbers.append(soup.find(id="sp2").text)
        numbers.append(soup.find(id="sp3").text)
        for i in range(1, 11):
            numbers.append(soup.find(id=f"ss{i}").text)
        for i in range(1, 11):
            numbers.append(soup.find(id=f"sc{i}").text)
        data = {
            "Number": numbers,
            "1st machine": [int(str(num)[0]) for num in numbers],
            "2nd machine": [int(str(num)[1]) for num in numbers],
            "3rd machine": [int(str(num)[2]) for num in numbers],
            "4th machine":  [int(str(num)[3]) for num in numbers]
        }
        df = pd.DataFrame(data)
        df.insert(0, "Date", np.nan, True)
        df.loc[0, "Date"] = f"{day}/{month}/{YEAR}"
        main_df = pd.concat([main_df, df], axis=0)
main_df.insert(6, "First prize", np.nan)
main_df.iloc[:len(first_winners), 6] = first_winners
main_df.to_excel("forfun.xlsx", index=False)

print("Generation has been completed")

