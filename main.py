import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv


with open("lottery.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Number1", "Number2", "Number3", "Number4", "Number5", "Number6", "Number7", "Date"])
headers = {"user-agent": UserAgent().chrome}

for year in range(2022, 2002, -1):
    url = f"https://www.lottery.co.za/lotto-plus-1/results/{year}"
    response = requests.get(url=url, headers=headers)
    bs_object = BeautifulSoup(response.content, "lxml")
    table = bs_object.find(name="table", class_="table lotto archiveTable").tbody.find_all(name="tr")
    for index in range(len(table)):
        date = table[index].td.text.strip().split(",")[1].strip()
        record = table[index].find(name="td", attrs={"style": "text-align: center; white-space: nowrap;"})
        numbers = record.find_all(name="div", class_="result small lotto-ball")
        numbers_value = [number.text.strip() for number in numbers]
        additional_number_value = record.find(name="div", class_="result small lotto-bonus-ball").text.strip()
        with open("lottery.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([numbers_value[0], numbers_value[1], numbers_value[2],
                             numbers_value[3], numbers_value[4], numbers_value[5],
                             additional_number_value, date])
