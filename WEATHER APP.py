import tkinter as tk
from tkinter import messagebox
import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = "7cd999a7a9c63ff9e13416b8515bed7f"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(location: str):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"An error occurred:\n{e}")
        return None

def on_get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city or ZIP code.")
        return

    result_label.config(text="Fetching weather...", fg="#6c5ce7")
    root.update_idletasks()

    data = get_weather(city)

    if not data:
        result_label.config(text="")
        return

    if data.get("cod") == 200:
        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"].title()

        location_label.config(text=f"{city_name}, {country}", fg="#00b894")
        temp_label.config(text=f"Temperature: {temp}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        condition_label.config(text=f"Condition: {condition}")
        result_label.config(text="")
    else:
        location_label.config(text="")
        temp_label.config(text="")
        humidity_label.config(text="")
        condition_label.config(text="")
        result_label.config(text="")
        messagebox.showerror("Error", data.get("message", "Unable to fetch weather data"))

root = tk.Tk()
root.title("Weather App")
root.geometry("320x320")
root.resizable(False, False)
root.configure(bg="#dfe6e9")

title_label = tk.Label(
    root,
    text="Weather App",
    font=("Segoe UI", 16, "bold"),
    bg="#dfe6e9",
    fg="white",
    pady=8
)
title_label.pack(fill="x")

input_frame = tk.Frame(root, bg="#dfe6e9")
input_frame.pack(pady=15)

city_label = tk.Label(input_frame, text="City or ZIP code:", bg="#dfe6e9", font=("Segoe UI", 10))
city_label.grid(row=0, column=0, padx=5)

city_entry = tk.Entry(input_frame, width=20, font=("Segoe UI", 10))
city_entry.grid(row=0, column=1, padx=5)

get_button = tk.Button(
    root,
    text="Get Weather",
    font=("Segoe UI", 11, "bold"),
    bg="#00b894",
    fg="white",
    activebackground="#00a37a",
    cursor="hand2",
    command=on_get_weather
)
get_button.pack(pady=5)

result_frame = tk.Frame(root, bg="#dfe6e9")
result_frame.pack(pady=10)

location_label = tk.Label(result_frame, text="", font=("Segoe UI", 12, "bold"), bg="#dfe6e9")
location_label.pack(pady=2)

temp_label = tk.Label(result_frame, text="", font=("Segoe UI", 11), bg="#dfe6e9")
temp_label.pack(pady=2)

humidity_label = tk.Label(result_frame, text="", font=("Segoe UI", 11), bg="#dfe6e9")
humidity_label.pack(pady=2)

condition_label = tk.Label(result_frame, text="", font=("Segoe UI", 11), bg="#dfe6e9")
condition_label.pack(pady=2)

result_label = tk.Label(root, text="", font=("Segoe UI", 10), bg="#dfe6e9")
result_label.pack(pady=5)

root.mainloop()
