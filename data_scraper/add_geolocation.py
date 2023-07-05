from geopy.geocoders import Nominatim
import pandas as pd 
import time

df = pd.read_csv('data/seven-11-storedata.csv')
file_path = "data/seven-11-geo.csv"
geolocator = Nominatim(user_agent="7-eleven-loc")


def main():
    address_list=get_address()
    lat = []
    lon = []
    time.sleep(0.5)
    count =0
    for address in address_list:
        print(f"{count} row is done")
        try: 
            location= get_geo(address)
            if location:
                lat.append(location.latitude)
                lon.append(location.longitude)
            else:
                lat.append(None)
                lon.append(None)
        except:
            lat.append(None)
            lon.append(None)
            print("something wrong")
        count+=1

    df['lat'] = lat
    df['lon'] = lon
    df.to_csv(file_path, index=False)
    print("File has been created!!")


def get_geo(address):
    location = geolocator.geocode(address)
    return location

def get_address():
    combined_list = df[['address', 'city', 'province']].apply(' '.join, axis=1).tolist()
    return combined_list

if __name__ == "__main__":
    main()

