import requests, json, os
from dotenv import load_dotenv



load_dotenv()
class NoSuchLocation(Exception):
    pass


API = os.getenv("API")

state = ""

key = ""

city = input("Enter city name: ")


def get_Location(city):
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=" + API + "&q=" + city + "&details=true&alias=" + state

    response = requests.get(location_url)

    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' + key + '?apikey=' + API + '&details=true'

    response = requests.get(conditions_url)
    json_version = response.json()

    weatherText = json_version[0].get('WeatherText')
    print("Current Conditions: " + weatherText)

    print('-----------------------------------------')


def get_5Dconditions(location_key):
    conditions5D_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + location_key + '?apikey=' + API + '&details=true'
    response = requests.get(conditions5D_url)
    json_version = response.json()
    for i in json_version["DailyForecasts"]:
        print("Forecast for:  " + i['Date'] + "   ")

        print("Low temperature: " + str(i['Temperature']['Minimum']['Value']))
        print("High temperature: " + str(i['Temperature']['Maximum']['Value']))

        print('-----------------------------------------')


try:
    location_key = get_Location(city)

    get_conditions(location_key)

    get_5Dconditions(location_key)
except NoSuchLocation:
    print("The location does not exists")
