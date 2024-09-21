
# Weather Fetcher

A Python-based desktop application to fetch and display the current weather and 5-day forecast for a selected city. The app also plots the temperature forecast using graphs. It uses the OpenWeatherMap API to fetch weather data and provides a dropdown for easy access to recent city searches.

## Features

- Fetches and displays the current weather for any city.
- Shows a 5-day weather forecast for the selected city.
- Plots a temperature forecast graph for the 5-day period.
- Stores the 5 most recent city searches and allows users to quickly select them from a dropdown.
- Built using Python's `Tkinter` for the GUI, `requests` for API calls, and `matplotlib` for graph plotting.
- Easy to use and modify for different weather APIs or GUI enhancements.

## Requirements

- Python 3.x
- OpenWeatherMap API key (sign up at [OpenWeatherMap](https://openweathermap.org/) to get a free API key)

### Python Libraries

This project uses the following Python libraries, which can be installed using `pip`:

- `requests`
- `tkinter` (comes with Python)
- `Pillow` (for image handling)
- `matplotlib` (for plotting graphs)
- `python-dotenv` (for managing environment variables)

Install the required libraries:

```bash
pip install requests pillow matplotlib python-dotenv
```

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/muxueya/WeatherFetcher.git
    cd WeatherFetcher
    ```

2. **Set up the `.env` file**:

   Create a `.env` file in the root directory and add your OpenWeatherMap API key:

   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **Run the application**:

   Simply run the Python script:

   ```bash
   python WeatherFetcher.py
   ```

## Usage

- **Enter City**: Type the name of the city you want to check the weather for, and click "Get Weather". 
- **Select Recent City**: After entering a city, it gets stored in a dropdown list. You can select a city from this dropdown to quickly fetch its weather data again.
- **Tabs**: The application provides three tabs:
  - **Current Weather**: Displays the current weather information for the selected city.
  - **5-Day Forecast**: Displays the weather forecast for the next 5 days.
  - **Temperature Graph**: Displays a plotted graph of the temperature forecast over the 5-day period.