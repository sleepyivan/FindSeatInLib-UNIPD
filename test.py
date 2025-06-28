import src.searchLib as searchLib

from datetime import datetime

url = "https://affluences.com/en/sites/biblioteca-beato-pellegrino/reservation"
date = datetime.today().strftime('%Y-%m-%d')

output = searchLib.parseLib(url, date)

print(output.head())  # Display the first few rows of the output DataFrame