import requests
import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime
from dotenv import load_dotenv
import os
import warnings

# Suppress iCCP warnings
warnings.filterwarnings("ignore", "(?s).*iCCP: known incorrect sRGB profile.*", category=UserWarning)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Initialize a list to store the recent cities
recent_cities = []

# Function to fetch the 5-day weather forecast from OpenWeatherMap API
def get_weather_forecast(city):
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    url = BASE_URL + 'q=' + city + '&appid=' + API_KEY + '&units=metric'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Function to update the recent cities list and dropdown
def update_recent_cities(city):
    # Add city to the list if not already in the list
    if city not in recent_cities:
        recent_cities.insert(0, city)  # Insert the city at the beginning
        if len(recent_cities) > 5:  # Keep only the last 5 entries
            recent_cities.pop()

    # Update the dropdown options
    city_menu['menu'].delete(0, 'end')  # Clear existing menu options
    for recent_city in recent_cities:
        city_menu['menu'].add_command(label=recent_city, command=tk._setit(city_var, recent_city, on_city_selected))

# Function to populate the input box with the selected city from the dropdown
def on_city_selected(selected_city):
    city_entry.delete(0, tk.END)
    city_entry.insert(0, selected_city)

# Function to plot the 5-day temperature forecast inside the tab
def plot_weather(data, tab_frame):
    dates = []
    temps = []

    for entry in data['list']:
        date = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
        temp = entry['main']['temp']
        dates.append(date)
        temps.append(temp)

    # Create a resized figure (smaller)
    fig = Figure(figsize=(7, 4), dpi=100)  # Resized graph to fit the window
    ax = fig.add_subplot(111)
    ax.plot(dates, temps, marker='o', color='#4CAF50')  # Green color matching the theme
    ax.set_title('5-Day Temperature Forecast', fontsize=14, fontweight='bold', color='#333333')
    ax.set_xlabel('Date and Time', fontsize=12, color='#333333')
    ax.set_ylabel('Temperature (°C)', fontsize=12, color='#333333')
    ax.grid(True, linestyle='--', color='#E0E0E0')
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", color='#333333')

    # Clear previous plot if any
    for widget in tab_frame.winfo_children():
        widget.destroy()

    # Embed the figure in the Tkinter tab using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=tab_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to handle the user input and display the current weather
def get_weather():
    city = city_entry.get()
    if city:
        # Get forecast data
        forecast_data = get_weather_forecast(city)

        if forecast_data:
            # Populate Current Weather tab
            current_weather = f"City: {city}\n" \
                              f"Temperature: {forecast_data['list'][0]['main']['temp']}°C\n" \
                              f"Weather: {forecast_data['list'][0]['weather'][0]['description']}\n" \
                              f"Humidity: {forecast_data['list'][0]['main']['humidity']}%\n" \
                              f"Wind Speed: {forecast_data['list'][0]['wind']['speed']} m/s"
            current_weather_label.config(text=current_weather)

            # Populate 5-Day Forecast tab
            forecast = ""
            for i in range(0, 40, 8):  # Every 8th entry (3-hour interval data, 8 per day)
                entry = forecast_data['list'][i]
                date = entry['dt_txt']
                temp = entry['main']['temp']
                description = entry['weather'][0]['description']
                forecast += f"{date}: {temp}°C, {description}\n"
            forecast_label.config(text=forecast)

            # Plot Temperature Forecast (in the graph tab)
            plot_weather(forecast_data, temp_graph_tab_frame)

            # Update the recent cities list
            update_recent_cities(city)
        else:
            messagebox.showerror("Error", f"Could not retrieve weather for {city}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

# Function to clear the input in the weather city box and all weather information in every tab
def clear_all():
    # Clear the city input field
    city_entry.delete(0, tk.END)

    # Clear weather information from all tabs
    current_weather_label.config(text="")  # Clear current weather tab
    forecast_label.config(text="")  # Clear forecast tab

    # Clear the temperature graph in the graph tab
    for widget in temp_graph_tab_frame.winfo_children():
        widget.destroy()

# Function to switch tabs and update colors
def show_frame(frame, button):
    # Raise the selected frame
    frame.tkraise()

    # Update tab button colors
    tab1_button.config(bg="light grey", fg="black")
    tab2_button.config(bg="light grey", fg="black")
    tab3_button.config(bg="light grey", fg="black")

    # Highlight the selected tab
    button.config(bg="light green", fg="black")

# Create the main Tkinter window
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("740x790")  # Increased window size to fit the graph
root.configure(bg="#F7F7F7")  # Light grey background for modern look

# Set the window icon to weather_icon.png
icon_image = Image.open("weather_icon.png")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)  # Set the icon of the window

# Resize the weather icon for display under the title (fixed size)
resized_icon_image = icon_image.resize((80, 80), Image.Resampling.LANCZOS)  # Fixed size 80x80
resized_icon_photo = ImageTk.PhotoImage(resized_icon_image)

# Title Label
title_label = tk.Label(root, text="Weather Fetcher", font=("Arial", 28, "bold"), background="#F7F7F7", foreground="#333333")
title_label.pack(pady=20)

# Add weather_icon.png under the title (fixed size)
icon_label = tk.Label(root, image=resized_icon_photo, background="#F7F7F7")
icon_label.pack(pady=10)

# Frame to hold both the input and recent cities dropdown
input_frame = tk.Frame(root, bg="#F7F7F7")
input_frame.pack(pady=10)

# City Input Field
city_label = tk.Label(input_frame, text="Enter City:", font=("Arial", 16), background="#F7F7F7", foreground="#333333")
city_label.grid(row=0, column=0, padx=10)

city_entry = tk.Entry(input_frame, width=20, font=("Arial", 16), relief="solid")
city_entry.grid(row=0, column=1, padx=10)

# Dropdown for Recent Cities
recent_city_label = tk.Label(input_frame, text="Select Recent City:", font=("Arial", 16), background="#F7F7F7", foreground="#333333")
recent_city_label.grid(row=1, column=0, padx=10)

city_var = StringVar()
city_var.set("Select Recent City")  # Default value

city_menu = OptionMenu(input_frame, city_var, "Select Recent City")
city_menu.config(width=20)  # Match the width of the input box
city_menu.grid(row=1, column=1, padx=10, pady=5)

# Add Get Weather and Clear Buttons using tk.Button
buttons_frame = tk.Frame(input_frame, bg="#F7F7F7")
buttons_frame.grid(row=0, column=2, rowspan=2, padx=20)

get_weather_button = tk.Button(buttons_frame, text="Get Weather", command=get_weather, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5, relief="raised", bd=3)
get_weather_button.pack(side=tk.TOP, padx=5)

clear_button = tk.Button(buttons_frame, text="Clear", command=clear_all, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5, relief="raised", bd=3)
clear_button.pack(side=tk.TOP, padx=5)

# Tab Frame (Manually created tabs using Frames)
tabs_frame = tk.Frame(root)
tabs_frame.pack(pady=10)

# Tab buttons
tab1_button = tk.Button(tabs_frame, text="Current Weather", command=lambda: show_frame(current_weather_tab, tab1_button), bg="light green", fg="black", font=("Arial", 12), padx=20, pady=5, relief="flat")
tab1_button.pack(side=tk.LEFT, padx=10)

tab2_button = tk.Button(tabs_frame, text="5-Day Forecast", command=lambda: show_frame(forecast_tab, tab2_button), bg="light grey", fg="black", font=("Arial", 12), padx=20, pady=5, relief="flat")
tab2_button.pack(side=tk.LEFT, padx=10)

tab3_button = tk.Button(tabs_frame, text="Temperature Graph", command=lambda: show_frame(graph_tab, tab3_button), bg="light grey", fg="black", font=("Arial", 12), padx=20, pady=5, relief="flat")
tab3_button.pack(side=tk.LEFT, padx=10)

# Create tab content frames
content_frame = tk.Frame(root, bg="#F7F7F7")
content_frame.pack(fill=tk.BOTH, expand=True)

current_weather_tab = tk.Frame(content_frame, bg="#F7F7F7")
forecast_tab = tk.Frame(content_frame, bg="#F7F7F7")
graph_tab = tk.Frame(content_frame, bg="#F7F7F7")

for frame in (current_weather_tab, forecast_tab, graph_tab):
    frame.grid(row=0, column=0, sticky="nsew")

# Centering content on each tab
for frame in (current_weather_tab, forecast_tab, graph_tab):
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

# Tab 1: Current Weather
current_weather_label = tk.Label(current_weather_tab, text="", font=("Arial", 14), background="#F7F7F7", foreground="#333333", justify="center")
current_weather_label.grid(row=0, column=0, pady=20)

# Tab 2: 5-Day Weather Forecast
forecast_label = tk.Label(forecast_tab, text="", font=("Arial", 14), background="#F7F7F7", foreground="#333333", justify="center")
forecast_label.grid(row=0, column=0, pady=20)

# Tab 3: 5-Day Temperature Forecast (Graph)
temp_graph_tab_frame = tk.Frame(graph_tab, bg="#F7F7F7")  # Set consistent background color
temp_graph_tab_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

# Start with the first tab visible
show_frame(current_weather_tab, tab1_button)

# Run the Tkinter main loop
root.mainloop()
