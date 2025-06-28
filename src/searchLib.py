# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

import numpy as np
import time

import pandas as pd

sleep_sec = np.round(np.random.uniform(0.5, 1.5), 2)

def parseLib(lib_url, date):
    lib_page = requests.get(lib_url)
    soup = BeautifulSoup(lib_page.content, 'html.parser')

    rooms_nodes = soup.select('ul li a')

    output = pd.DataFrame()

    def parseRoom(room_url):
        time.sleep(sleep_sec)  # To avoid overwhelming the server

        room_page = requests.get(room_url)
        soup = BeautifulSoup(room_page.content, 'html.parser')

        room_name = soup.select_one('h1').get_text(strip=True)
        output = {'room_name': room_name, 'date': date, 'seat_name': [], 'availability': []}

        seats_nodes = soup.select('app-search-resource app-results ul li')

        def parseSeat(seat_node):
            seat_name = seat_node.select_one('h2').get_text(strip=True)
            availability = seat_node.select('app-available-resource-time-slots > div:first-child button:not([disabled]) time')
            availability = [time.get('datetime') for time in availability]
            return seat_name, availability

        for seat_node in seats_nodes:
            seat_name, availability = parseSeat(seat_node)
            output['seat_name'].append(seat_name)
            output['availability'].append(availability)

        return pd.DataFrame(output)

    for room_node in rooms_nodes:
        room_url = 'https://affluences.com' + room_node.get('href') + '&date=' + date
        room_df = parseRoom(room_url)
        output = pd.concat([output, room_df], ignore_index=True)

    return output