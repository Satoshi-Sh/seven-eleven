import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd

base_url = "https://stores.7-eleven.ca"
file_path = "data/seven-11-storedata.csv"

def main():
    canada_dic =get_provinces()
    all_cities = []
    for province in canada_dic:
        all_cities.extend(get_cities(province))
    all_stores = []
    for city in all_cities:
        all_stores.extend(get_stores(city))
    df = pd.DataFrame(all_stores)
    df.to_csv(file_path, index=False)
    print("File has been created!!")

def get_stores(city):
    stores = []
    time.sleep(0.3)
    response = requests.get(base_url +'/' + city['link'])
    soup = BeautifulSoup(response.content, "html.parser")
    class_name = "Teaser"
    hour_name = "data-days"
    elements = soup.findAll("div",class_=class_name)
    for element in elements:
        address = element.find('a').text
        hours = json.loads(element.find('span', class_='c-hours-today').get(hour_name))
        stores.append({"address":address,"hours":hours,"city":city['city'],"province":city['province']})
    return stores


def get_provinces():
    response = requests.get(base_url +'/ca')
    soup = BeautifulSoup(response.content, "html.parser")
    class_name = "Directory-listItem"
    elements = soup.findAll("li",class_=class_name)
    canada_dic = []
    for element in elements:
        store_count= int(element.find('a').get('data-count')[1:-1])
        province = element.find('span').text
        href= element.find('a').get('href')
        canada_dic.append({"province":province,"store_counts":store_count,"link":href})
    print(canada_dic)
    return canada_dic

def get_cities(province):
    cities =[]
    class_name = "Directory-listItem"
    time.sleep(0.2)
    city_url = base_url + '/' + province['link']
    response = requests.get(city_url)
    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.findAll('li', class_=class_name)
    for element in elements:
       store_count= int(element.find('a').get('data-count')[1:-1])
       city = element.find('span').text.capitalize()
       href= element.find('a').get('href')[2:]
       cities.append({"store_count":store_count,'city':city,'link':href,'province':province["province"]})
    print(cities)
    return cities

if __name__ == "__main__":
    main()



