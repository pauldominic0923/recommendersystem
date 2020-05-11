from flask import Flask, jsonify, request, render_template
import numpy as np
import pandas as pd
import requests
import json
import os 
from pandas.io.json import json_normalize
# import configparser

app = Flask(__name__)
# app.config.from_envvar('APP_SETTINGS')

# config = configparser.ConfigParser()
# config.read('config.cfg')
# print(config['GOOGLE.MAPS']['SECRET_KEY'])

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template("index.html")

@app.route('/hello', methods=['GET', 'POST'])
def hello():
	# POST request: goes from browser to flask
    if request.method == 'POST':
    	# print('Incoming..')
    	jsonData = request.get_json(force=True)
    	# print(jsonData.get('greeting'))  # parse as JSON
    	return str(jsonData.get('greeting')), 200

    # GET request: goes from flask to browser
    else :
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/cityWeather', methods=['GET', 'POST'])
def cityWeather():
    if request.method == 'POST':
    	jsonData = request.get_json(force=True)
    	city = str(jsonData.get('city'))
    	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=3739750b9f8a52c079de7d8292030d35&units=metric'.format(city)
    	res = requests.get(url)
    	data = res.json()
    	return data, 200 

@app.route('/recommendation', methods=['GET', 'POST'])
def getWeather():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        temperature = jsonData.get('temperature')
        precipitation = str(jsonData.get('precipitation'))

        if temperature == "none":
            weatherLabel = "weathernotfound"
        else:
            temperature = int(temperature)

        if isinstance(temperature, (int, float)):
            if temperature <= 0 and (precipitation == "Clear" or precipitation == "Clouds"):
                weatherLabel = "colddry"
            elif temperature <= 0 and (precipitation == "Rain" or precipitation == "Drizzle" or precipitation == "Thunderstorm" or precipitation == "Mist" or precipitation == "Fog"):
                weatherLabel = "coldrain"
            elif temperature <= 0 and precipitation == "Snow":
                weatherLabel = "coldsnow"
            elif temperature > 0 and temperature <18 and (precipitation == "Clear" or precipitation == "Clouds"):
                weatherLabel = "chillydry"
            elif temperature > 0 and temperature <18 and (precipitation == "Rain" or precipitation == "Drizzle" or precipitation == "Thunderstorm" or precipitation == "Mist" or precipitation == "Fog"):
                weatherLabel = "chillyrain"
            elif temperature > 0 and temperature <18 and precipitation == "Snow":
                weatherLabel = "chillysnow"
            elif temperature >=18 and temperature <25 and (precipitation == "Clear" or precipitation == "Clouds"):
                weatherLabel = "warmdry"
            elif temperature >=18 and temperature <25 and (precipitation == "Rain" or precipitation == "Drizzle" or precipitation == "Thunderstorm" or precipitation == "Mist" or precipitation == "Fog"):
                weatherLabel = "warmrain"
            elif temperature >25 and (precipitation == "Clear" or precipitation == "Clouds"):
                weatherLabel = "hotdry"
            elif temperature > 25 and (precipitation == "Rain" or precipitation == "Drizzle" or precipitation == "Thunderstorm" or precipitation == "Mist" or precipitation == "Fog"):
                weatherLabel = "hotrain"
  
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "nordstrom.json")
        nordsdata = json.load(open(json_url))

        df = pd.DataFrame(nordsdata[0]['clothing'])

        No_Reviews = df['reviews']
        Rating = df['rating']

        df['weighted_rating'] = (0.5*Rating) + (5*(1-0.5))*(1-(np.exp((-No_Reviews)/50)))

        weighted_rating = df['weighted_rating']
        df['discount_percent'] = pd.to_numeric(df['discount_percent'],errors='coerce')
        discount_percent = df['discount_percent']

        p = 0.7
        df['weighted_discount'] = (p*(weighted_rating)) + (5*(1-p))*(1-(np.exp(((-discount_percent)/20))))

        df = df.sort_values(by = ['weighted_discount', 'price'], ascending = [False, True])
        df = df.drop_duplicates(subset = ['name'])
        df = df[~df.name.str.contains("nursing|maternity", case = False)]

        colddry = df[df.category.str.contains('hoodie| sweaters|jeans|pants|blazers|coats',case=False)]
        coldrain = df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
        coldsnow= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
        chillydry= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
        chillyrain= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
        chillysnow= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
        warmdry= df[df.category.str.contains('shorts|polo|jeans| hoodie| t-shirt| dress |romper|top|sweater',case=False)]
        warmrain = df[df.category.str.contains('shorts|polo|jeans| hoodie| t-shirt|dress|romper|top|sweater ',case=False)]
        hotdry= df[df.category.str.contains('shorts|polo|jeans|tank|shirts|dress|romper|top|swimsuit',case=False)]
        hotrain= df[df.category.str.contains('shorts|polo|jeans|tank|shirts|dress|romper|top|swimsuit',case=False)]

        if weatherLabel == "colddry": 
            colddrymale = colddry[colddry['gender'].isin(['MALE'])]
            colddrymale = colddrymale.drop_duplicates(subset = ['category'])
            colddryfemale = (colddry[colddry['gender'].isin(['FEMALE'])])
            colddryfemale = colddryfemale.drop_duplicates(subset = ['category'])
            sort_colddry = pd.concat([colddrymale.head(3), colddryfemale.head(3)])

            return sort_colddry.to_json(orient='records')
        elif weatherLabel == "coldrain":
            coldrainmale = coldrain[coldrain['gender'].isin(['MALE'])]
            coldrainmale = coldrainmale.drop_duplicates(subset = ['category'])
            coldrainfemale = (coldrain[coldrain['gender'].isin(['FEMALE'])])
            coldrainfemale = coldrainfemale.drop_duplicates(subset = ['category'])
            sort_coldrain = pd.concat([coldrainmale.head(3), coldrainfemale.head(3)])

            return sort_coldrain.to_json(orient='records')
        elif weatherLabel == "coldsnow":
            coldsnowmale = coldsnow[coldsnow['gender'].isin(['MALE'])]
            coldsnowmale = coldsnowmale.drop_duplicates(subset = ['category'])
            coldsnowfemale = (coldsnow[coldsnow['gender'].isin(['FEMALE'])])
            coldsnowfemale = coldsnowfemale.drop_duplicates(subset = ['category'])
            sort_coldsnow = pd.concat([coldsnowmale.head(3), coldsnowfemale.head(3)])

            return sort_coldsnow.to_json(orient='records')
        elif weatherLabel == "chillydry":
            chillydrymale = chillydry[chillydry['gender'].isin(['MALE'])]
            chillydrymale = chillydrymale.drop_duplicates(subset = ['category'])
            chillydryfemale = (chillydry[chillydry['gender'].isin(['FEMALE'])])
            chillydryfemale = chillydryfemale.drop_duplicates(subset = ['category'])
            sort_chillydry = pd.concat([chillydrymale.head(3), chillydryfemale.head(3)])

            return sort_chillydry.to_json(orient='records')
        elif weatherLabel == "chillyrain":
            chillyrainmale = chillyrain[chillyrain['gender'].isin(['MALE'])]
            chillyrainmale = chillyrainmale.drop_duplicates(subset = ['category'])
            chillyrainfemale = (chillyrain[chillyrain['gender'].isin(['FEMALE'])])
            chillyrainfemale = chillyrainfemale.drop_duplicates(subset = ['category'])
            sort_chillyrain = pd.concat([chillyrainmale.head(3), chillyrainfemale.head(3)])

            return sort_chillyrain.to_json(orient='records')
        elif weatherLabel == "chillysnow":
            chillysnowmale = chillysnow[chillysnow['gender'].isin(['MALE'])]
            chillysnowmale = chillysnowmale.drop_duplicates(subset = ['category'])
            chillysnowfemale = (chillysnow[chillysnow['gender'].isin(['FEMALE'])])
            chillysnowfemale = chillysnowfemale.drop_duplicates(subset = ['category'])
            sort_chillysnow = pd.concat([chillysnowmale.head(3), chillysnowfemale.head(3)])

            return sort_chillysnow.to_json(orient='records')
        elif weatherLabel == "warmdry":
            warmdrymale = warmdry[warmdry['gender'].isin(['MALE'])]
            warmdrymale = warmdrymale.drop_duplicates(subset = ['category'])
            warmdryfemale = (warmdry[warmdry['gender'].isin(['FEMALE'])])
            warmdryfemale = warmdryfemale.drop_duplicates(subset = ['category'])
            sort_warmdry = pd.concat([warmdrymale.head(3), warmdryfemale.head(3)])

            return sort_warmdry.to_json(orient='records')
        elif weatherLabel == "warmrain":
            warmrainmale = warmrain[warmrain['gender'].isin(['MALE'])]
            warmrainmale = warmrainmale.drop_duplicates(subset = ['category'])
            warmrainfemale = (warmrain[warmrain['gender'].isin(['FEMALE'])])
            warmrainfemale = warmrainfemale.drop_duplicates(subset = ['category'])
            sort_warmrain = pd.concat([warmrainmale.head(3), warmrainfemale.head(3)])

            return sort_warmrain.to_json(orient='records')
        elif weatherLabel == "hotdry":
            hotdrymale = hotdry[hotdry['gender'].isin(['MALE'])]
            hotdrymale = hotdrymale.drop_duplicates(subset = ['category'])
            hotdryfemale = (hotdry[hotdry['gender'].isin(['FEMALE'])])
            hotdryfemale = hotdryfemale.drop_duplicates(subset = ['category'])
            sort_hotdry = pd.concat([hotdrymale.head(3), hotdryfemale.head(3)])

            return sort_hotdry.to_json(orient='records')
        elif weatherLabel == "hotrain":
            hotrainmale = hotrain[hotrain['gender'].isin(['MALE'])]
            hotrainmale = hotrainmale.drop_duplicates(subset = ['category'])
            hotrainfemale = (hotrain[hotrain['gender'].isin(['FEMALE'])])
            hotrainfemale = hotrainfemale.drop_duplicates(subset = ['category'])
            sort_hotrain = pd.concat([hotrainmale.head(3), hotrainfemale.head(3)])

            return sort_hotrain.to_json(orient='records')
        elif weatherLabel == "weathernotfound":
            noweathermale = df.drop_duplicates(subset = ['category'])
            noweathermale = df[df['gender'].isin(['MALE'])]
            noweatherfemale = (df[df['gender'].isin(['FEMALE'])])
            noweatherfemale = df.drop_duplicates(subset = ['category'])
            sort_noweather = pd.concat([noweathermale.head(3), noweatherfemale.head(3)])

            return sort_noweather.to_json(orient='records')


# @app.route('/googleMaps', methods=['GET', 'POST'])
# def googleMaps():
#     if request.method == 'POST':
#         print("POST request")

#     else:
#         googleMapsAPI = config['GOOGLE.MAPS']['SECRET_KEY']
#         return googleMapsAPI
        
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
