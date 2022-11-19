"""
Infinite pain and suffer (OwO)

@author: Saplyn Miao
"""

import tkinter as tk
import requests
from datetime import datetime

def TimeFormater(_time:int):
    return datetime.utcfromtimestamp(_time).time()

def ClearMonolog() -> None:
    info_outputbox.delete("1.0", tk.END)
    return

def OutputFiller() -> None:
    # -- Weather Fetcher  --
    # API key
    apikey_str:str = "26c42f2d6bd3609e2139308527124e6a"
    # Clear the output box
    ClearMonolog()
    # Fetch weather info
    location_str:str = cityInfo_str.get()
    weather_url:str = f"http://api.openweathermap.org/data/2.5/weather?q={location_str}&appid={apikey_str}&units=metric"
    weather_respose = requests.get(weather_url)
    directFetchFail_bool:bool = False
    if not weather_respose.ok:
        directFetchFail_bool = True
        location_url:str = f"http://api.openweathermap.org/geo/1.0/direct?q={location_str}&appid={apikey_str}"
        location_respose = requests.get(location_url)
        if location_respose.json() != []:
            location_info = location_respose.json()
            lat = location_info[0]["lat"]
            lon = location_info[0]["lon"]
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey_str}&units=metric"
            weather_respose = requests.get(weather_url)
        else:
            totalOutput_str:str = f"\n"
            totalOutput_str += f"[Location Corrector]\n"
            totalOutput_str += f"Couldn't find \"{location_str}\", and we failed to correct it.\n"
            info_outputbox.insert(tk.INSERT, totalOutput_str)
            return
    weather_info = weather_respose.json()
    # Classify things
    requestedCity_str:str = weather_info["name"]
    weatherOverall_str:str = weather_info["weather"][0]["main"]
    weatherDescription_str:str = weather_info["weather"][0]["description"]
    temperature_flt:float = weather_info["main"]["temp"]
    temperatureFeel_flt:float = weather_info["main"]["feels_like"]
    timezone_int:int = weather_info["timezone"]
    sunrise_time = TimeFormater(weather_info["sys"]["sunrise"] + timezone_int)
    sunset_time = TimeFormater(weather_info["sys"]["sunset"] + timezone_int)
    currentTime_time = TimeFormater(weather_info["dt"] + timezone_int)
    # Push the weather info
    totalOutput_str:str = f"\n"
    if directFetchFail_bool:
        totalOutput_str += f"[Location Corrector]\n"
        totalOutput_str += f"Couldn't find \"{location_str}\", did you mean \"{requestedCity_str}\"?\n\n"
    totalOutput_str += f"[Weather of {requestedCity_str}]\n"
    totalOutput_str += f"It's {currentTime_time} now in {requestedCity_str}.\n"
    totalOutput_str += f"The temperature there is {temperature_flt}℃, and it feels like {temperatureFeel_flt}℃.\n"
    totalOutput_str += f"The general weather is: {weatherOverall_str}, for detailed: {weatherDescription_str}.\n"
    totalOutput_str += f"the sun rises at {sunrise_time} and sets at {sunset_time}.\n"
    # Flush!
    info_outputbox.insert(tk.INSERT, totalOutput_str)
    # -- Activity Advisor --
    totalOutput_str = f"\n"
    totalOutput_str += f"[Activity Advisor]\n"
    # What to wear
    if temperature_flt < 0:
        totalOutput_str += "Cloth: Put on your thick coat!\n"
    elif temperature_flt < 5:
        totalOutput_str += "Cloth: Arm yourself with a sweater~"
    elif temperature_flt < 10:
        totalOutput_str += "Cloth: Wear something that can keep you warm~\n"
    elif temperature_flt < 15:
        totalOutput_str += "Cloth: Take a lite jacket with you, just in case.\n"
    elif temperature_flt < 20:
        totalOutput_str += "Cloth: Short sleeve should be fine~\n"
    else:
        totalOutput_str += "Cloth: Wear something \"chilly\"~ (^w^)\n"
    # Take sth with you
    if weatherOverall_str == "Rain":
        totalOutput_str += "Carry: It's raining outside, take an umbrella!\n"
    elif weatherOverall_str == "Snow":
        totalOutput_str += "Carry: It's snowing outside, take an umbrella!\n"
    elif weatherOverall_str == "Clear":
        totalOutput_str += "Carry: Clear sky outside, sunscream may needed!\n"
    else:
        totalOutput_str += "Carry: Wear a happy face~ (>w<)\n"
    # P.E. class availability
    if weatherOverall_str == "Rain":
        totalOutput_str += "Sport: You may reserve a place indoor if you wanna work \"out\".\n"
        totalOutput_str += "       P.E. class may cancel, conduct your teacher to stay up-to-date.\n"
    elif weatherOverall_str == "Snow":
        totalOutput_str += "Sport: You may reserve a place indoor if you wanna work \"out\".\n"
        totalOutput_str += "       P.E. class may cancel, conduct your teacher to stay up-to-date.\n"
    else:
        totalOutput_str += "Sport: Purrfect weather for sports!\n"
        totalOutput_str += "       P.E. class won't cancel, enjoy your day!\n"
    # Flush!
    info_outputbox.insert(tk.INSERT, totalOutput_str)
    return

def ActivityAdvisor():
    return

root = tk.Tk()
root.title("Weather Cat for University Students")
root.geometry("700x520")

intro_lable = tk.Label(root, text="Location", fg="Orange", bg="White", font=("Times", 20))
intro_lable.pack(pady=20)

cityInfo_str:str = tk.StringVar()
location_inputbox = tk.Entry(root, textvariable=cityInfo_str, width=24, font=("Times",16))
location_inputbox.pack()

search_button = tk.Button(root, command=OutputFiller, text="Search", font=('Times', 16))
search_button.pack(pady=10)

clear_button = tk.Button(root, command=ClearMonolog, text="Clear", font=("Times", 16))
clear_button.pack(padx=5, side=tk.RIGHT)

info_lable = tk.Label(root, text="Weather Infomation", fg="Orange", bg="White", font=("Times", 20))
info_lable.pack(pady=10)

info_outputbox = tk.Text(root, width=70, height=17)
info_outputbox.pack()

root.mainloop()
