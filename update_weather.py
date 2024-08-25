from datetime import datetime

import requests
from colorama import Fore, init

# init colorama
init()

data_string = ""

is_day = True

# Define the URL for the weather data
url = "https://wttr.in/canberra?format=j1"


def get_json():
    try:
        # Make a GET request to fetch the data
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        global weather_data
        # Get the JSON content from the response
        weather_data = response.json()

        # Save the JSON content to a file
        # file_path = "weather.json"
        # with open(file_path, "w") as file:
        # json.dump(weather_data, file, indent=4)

        # print(f"Weather data saved successfully to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weather data. Error: {e}")


def init_nerd_map():
    global weather_nerd_day
    global weather_nerd_night

    weather_nerd_day = {
        113: "",  # 晴
        116: "",  # 少云
        119: "",  # 多云
        122: "",  # 阴
        143: "",  # 轻雾
        176: "",  # 局部小雨
        182: "",  # 局部小雪
        200: "",  # 可能打雷
        263: "",  # 局部毛毛雨
        # TODO: Others wait to add
    }
    weather_nerd_night = {
        113: "",
        116: "",
        119: "",
        122: "",  # 阴
        143: "",
        176: "",  # 局部小雨
        182: "",
        200: "",
        263: "",
        # TODO: Others wait to add
    }


def update_day_night():
    time_format = "%I:%M %p"
    global current_time
    current_time = datetime.now().time()
    global sun_set
    global sun_rise
    sun_set = datetime.strptime(
        weather_data["weather"][0]["astronomy"][0]["sunset"], time_format
    ).time()

    sun_rise = datetime.strptime(
        weather_data["weather"][0]["astronomy"][0]["sunrise"], time_format
    ).time()

    global is_day
    if current_time < sun_set and current_time > sun_rise:
        is_day = True
    else:
        is_day = False
    print(current_time)
    print(sun_set)
    print(sun_rise)


# Get current weather prediction
def predict_weather():
    index = []
    global current_time

    # Get weather prediction on 6 am, 9 am, 12 pm, 3 pm, 6 pm, and 9 pm
    # and add to displayed string based on the current time
    if current_time.hour < 6:
        index.append(2)
    if current_time.hour < 9:
        index.append(3)
    if current_time.hour < 12:
        index.append(4)
    if current_time.hour < 15:
        index.append(5)
    if current_time.hour < 18:
        index.append(6)
    if current_time.hour < 21:
        index.append(7)

    for i in index:
        if i == 7 or (i == 6 and sun_set.hour < 18):
            map = weather_nerd_night
        else:
            map = weather_nerd_day
        weather_code = weather_data["weather"][0]["hourly"][i]["weatherCode"]
        temperature = int(weather_data["weather"][0]["hourly"][i]["tempC"])

        if temperature < 0:
            color = Fore.MAGENTA
        elif temperature < 10:
            color = Fore.BLUE
        elif temperature < 20:
            color = Fore.GREEN
        elif temperature < 30:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        global data_string
        data_string += color + map[int(weather_code)] + " " + str(temperature) + "°C "

        if int(weather_data["weather"][0]["hourly"][i]["chanceofrain"]) != 0:
            data_string += (
                color
                + " "
                + weather_data["weather"][0]["hourly"][i]["chanceofrain"]
                + "%% "
            )
        if int(weather_data["weather"][0]["hourly"][i]["chanceofsnow"]) != 0:
            data_string += (
                color
                + " "
                + weather_data["weather"][0]["hourly"][i]["chanceofrain"]
                + "%% "
            )


# Add colour to current weather condition
def current_weather():
    if is_day:
        map = weather_nerd_day
    else:
        map = weather_nerd_night

    weather_code = weather_data["current_condition"][0]["weatherCode"]
    temperature = int(weather_data["current_condition"][0]["temp_C"])

    if temperature < 0:
        color = Fore.MAGENTA
    elif temperature < 10:
        color = Fore.BLUE
    elif temperature < 20:
        color = Fore.GREEN
    elif temperature < 30:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    global data_string
    data_string += Fore.WHITE + "| "
    data_string += color + map[int(weather_code)] + " " + str(temperature) + "°C"

    uvi = int(weather_data["current_condition"][0]["uvIndex"])

    if uvi < 2:
        color = Fore.GREEN
    elif uvi <= 5:
        color = Fore.YELLOW
    elif uvi <= 7:
        color = Fore.RED
    else:
        color = Fore.MAGENTA

    data_string += color + " 󰓠 " + str(uvi)

    data_string += Fore.WHITE + " | "


# Define whether to display sunrise or sunset
def sunrise_sunset():
    global data_string
    global sun_set
    global sun_rise
    data_string += Fore.WHITE + "| "
    if is_day:
        data_string += Fore.YELLOW + " " + str(sun_set.strftime("%H:%M"))
    else:
        data_string += Fore.YELLOW + " " + str(sun_rise.strftime("%H:%M"))
    data_string += Fore.RESET


def save_file():
    file_path = "/Users/noahliucn/.config/weather.txt"
    with open(file_path, "w+") as file:
        file.write(data_string)


if __name__ == "__main__":
    get_json()
    update_day_night()
    init_nerd_map()
    current_weather()
    predict_weather()
    sunrise_sunset()
    save_file()
    print(is_day)
