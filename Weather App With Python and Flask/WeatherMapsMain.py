from datetime import date
from OpenWeatherMapsApi import WeatherMapsApi
from WeatherMapsController import WeatherMapsControl
from TemptureConversion import ConvertTemperature
from CityErrorValidation import ValidationOfCity
from CityStateValidation import ValidatingState
from flask import Flask , render_template ,request,jsonify, redirect, url_for,flash

#DSC 510
#Week 12
#Final Project
#Programming Assignment Week 12
#Author Felipe Castillo
#06/03/2021

#Final Check List
'''
- You must show at a bare minimum the following weather information
Current Temp: 47.35 degrees
High Temp: 50 degrees
Low Temp: 44.01 degrees
Pressure: 1019hPa
Humidity: 40%

- You must allow the user to enter in a city and a zip code
- You must have a really good interface
- You MUST NOT display temp in Kelvin (this is not readable for most users)
- Think of weather.com and what level of data and how the interface looks.  Make sure that it is usable
- You MUST NOT print JSON data to the screen.
- You must show the user the city they're requesting.  If the user inputs 68138 you should say weather for Omaha NE.

Working Example
Would you like to lookup weather data by US City or zip code? Enter 1 for US City 2 for zip: 1
Please enter the city name: omaha
Please enter the state abbreviation: ne
Would you like to view temps in Fahrenheit, Celsius, or Kelvin.
Enter 'F' for Fahrenheit, 'C' for Celsius, 'K' for Kelvin: f

EXAMPLE OUT PUT
Current Temp: 47.35 degrees
High Temp: 50 degrees
Low Temp: 44.01 degrees
Pressure: 1019hPa
Humidity: 40%
Cloud Cover: Minimual Cloud Cover
Would you like to perform another weather lookup? (Y/N)
'''

'''
Notes to professor
If user doesnt not insert the correct city a suggestion will be provided
If city and state can be validate no abbrevation will be provided
If user doesnt provide a temp for the radio button it will set it to F as default
If user misspells or doesnt insert correct values errors are validated by ZIP and CITY
'''


app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'BASE_REPLAY'
weather_data = []


def date_time_today():
    today = date.today()
    reformattedDate = today.strftime("%B-%d-%Y")
    return reformattedDate

def cloud_percentage_scale_amount(weather_session):
    cloud_description = ''
    clouds = weather_session.weatherClouds
    if(clouds > 0 and clouds <= 25):
        cloud_description = 'Minimal Clouds'
    elif(clouds > 25 and clouds <= 50):
        cloud_description = 'Mid Minimal Clouds'
    elif(clouds > 50 and clouds <= 75):
        cloud_description = 'Higher Then Average Clouds'
    else:
        cloud_description = 'Very High Amount of Clouds'
    return cloud_description


def temperature_type_scale(temperatureType,temperature_scale,weather_session):
    regularTemperature = ''
    maxTemp = ''
    minTemp = ''
    symbol = ''
    if(len(temperatureType) != 0):  # Checking to make sure the list is not empty
        if(temperatureType[0] == 'F'):
            regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
            symbol = '°F'
        elif(temperatureType[0] == 'C'):
            regularTemperature = temperature_scale.kelvinToCelsius(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToCelsius(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToCelsius(weather_session.weatherTemMin)
            symbol = '°C'
        elif(temperatureType[0] == 'K'):
            regularTemperature = weather_session.weatherTempature
            maxTemp = weather_session.weatherTemMax
            minTemp = weather_session.weatherTemMin
            symbol = '°K'
        else: # If user doesnt choose a type Default is Fahrenherit
            regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
            symbol = '°F'
    else: #when the program runs if prevoius data exists it poplates old data until new data is present bt default always Fahrenheit
        regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
        maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
        minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
        symbol = '°F'

    return  regularTemperature,maxTemp,minTemp,symbol


def conntect_api_weather(city):
    json_object = ''
    weatherRequest = WeatherMapsApi(city)
    if(city.isnumeric()):
        url = weatherRequest.weather_url_zipCode()
        json_object = weatherRequest.JsonData(url)
    else:
        url = weatherRequest.weather_url_word()
        json_object = weatherRequest.JsonData(url)
    return json_object


def city_validation(json_object):
    try:
        cityFlag = ValidationOfCity(json_object)
        status = cityFlag.status_code()
        return status
    except:
        print("Couldnt validate city!")


def weather_call(city):# making sure api connected correctly
    flag_city = ''
    try:
        json_object = conntect_api_weather(city)
        cityFlag = city_validation(json_object) # making sure user inserts a correct city
        if(cityFlag == False):
            flag_city = False
        else:
            flag_city = True
    except:
        print("Failed To Find Data information")
    return flag_city


@app.errorhandler(500)
def server_issue(expecption):
    print(expecption)

    return render_template("500.html")

@app.errorhandler(404)
def server_issue(expecption):
    print(expecption)

    return render_template("404.html")

@app.route("/")
def root():
    return redirect(url_for('Find_Weather'))


@app.route("/Find_Weather", methods=['GET','POST'])
def Find_Weather():
    try:
        city = ''
        weather = ''
        error = True
        abbrevation = ''
        temperatureType = ''
        todaysDate = date_time_today()
        if request.method == 'POST':
            city = request.form.get('city_Lookup')
            abbrevation = request.form.get('state_Lookup')
            temperatureType = request.form.getlist('option')
        weather = weather_call(city)
        if not weather: #validated city return a good status
            json_object = conntect_api_weather(city) #Felipe Castillo
            weather_session = WeatherMapsControl(json_object)

            if weather_session.weatherName != None:
                state_abbrevation_confirmed = ''
                verfied_state = ValidatingState()

                if(abbrevation != ""): #user provids a abbrevation, making sure user doesnt use an incorrect abbrevation

                    state = verfied_state.abv_state_record(abbrevation)
                    confirmed_state = verfied_state.state_with_abv_look_up(weather_session.weatherName, state) #validated abv belongs to state
                    state_abbrevation_confirmed = verfied_state.state_abv_lookup(confirmed_state) # returning confirmed abv

                if(state_abbrevation_confirmed == "" and abbrevation!= ""): # if abbrevation is not validated it means it incorrect will look to find a suggestion, suggestion will be provided
                   state = verfied_state.state_look_up(weather_session.weatherName)
                   state_abbrevation_confirmed = verfied_state.state_abv_lookup(state) + "-" + "Suggested"


                temperature_scale = ConvertTemperature() # Converting temperature to usr selection

                temperatures_scale_Returned = temperature_type_scale(temperatureType,temperature_scale,weather_session) # get the temperature according to user choice
                normalTemp = str(temperatures_scale_Returned).split(",")[0].replace("(","").strip()
                maxTemp = str(temperatures_scale_Returned).split(",")[1].replace("(", "").strip()
                minTemp = str(temperatures_scale_Returned).split(",")[2].replace("(", "").strip()
                symbol = str(temperatures_scale_Returned).split(",")[3].replace(")", "").strip()

                cloud_amount_sky = cloud_percentage_scale_amount(weather_session) # getting a converted decription of cloud coverage per the percetage in weather session object per city


                weatherInfo = {
                    'city': weather_session.weatherName+", "+state_abbrevation_confirmed,
                    'temperature': normalTemp+ " "+ symbol,
                    'temperature_max': maxTemp+ " "+ symbol,
                    'temperature_min': minTemp+" "+ symbol,
                    'pressure': str(weather_session.weatherPressure)+" hPa",
                    'humidity': str(weather_session.weatherHumidity)+ "%",
                    'cloud_amount' : cloud_amount_sky,
                    'icon': weather_session.weatherIcon
                }
                error = False
                weather_data.append(weatherInfo)

        else:
            error = True
            weatherInfo = {
                'city': "",
                'temperature': "",
                'temperature max': "",
                'temperature min': "",
                'pressure': "",
                'humidity': "",
                'cloud_amount':"",
                 'icon': ""}
            error_message = 'Error message'
        if error:
            errorTpye = ''
            if city.isnumeric():
                errorTpye = 'ZIP CODE'
            else:
                errorTpye = 'CITY'
            flash("Please insert a correct "+ errorTpye + " this is invalid. Please retype or check spelling", 'error')

        return render_template("index.html", weatherInfo=weatherInfo, todaysDate=todaysDate)
    except:
        print("Could not load website possible 500 internet error.")




if __name__ == '__main__':
    app.run()
