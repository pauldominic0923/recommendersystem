import json 
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

##weather labels: cold, chilly, warm, hot
##precipitation labels: dry, rain, snow

def getWeather(temperature = 9, precipitation = 'rain'):
    if temperature <= 0 and precipitation == 'clear sky' or precipitation == 'few clouds' or precipitation == 'scattered clouds' or precipitation == 'broken clouds':
        weatherLabel = "colddry"
    elif temperature <= 0 and precipitation == 'rain' or precipitation == 'shower rain' or precipitation == 'thunderstorm' or precipitation == 'mist':
        weatherLabel = "coldrain"
    elif temperature <= 0 and precipitation == 'snow':
        weatherLabel = "coldsnow"
    elif temperature > 0 and temperature <10 and precipitation == 'clear sky' or precipitation == 'few clouds' or precipitation == 'scattered clouds' or precipitation == 'broken clouds':
        weatherLabel = "chillydry"
    elif temperature > 0 and temperature <10 and precipitation == 'rain' or precipitation == 'shower rain' or precipitation == 'thunderstorm' or precipitation == 'mist':
        weatherLabel = "chillyrain"
    elif temperature > 0 and temperature <10 and precipitation == 'snow':
        weatherLabel = "chillysnow"
    elif temperature >=10 and temperature <20 and precipitation == 'clear sky' or precipitation == 'few clouds' or precipitation == 'scattered clouds' or precipitation == 'broken clouds':
        weatherLabel = "warmdry"
    elif temperature >=10 and temperature <20 and precipitation == 'rain' or precipitation == 'shower rain' or precipitation == 'thunderstorm' or precipitation == 'mist':
        weatherLabel = "warmrain"
    elif temperature >20 and precipitation == 'clear sky' or precipitation == 'few clouds' or precipitation == 'scattered clouds' or precipitation == 'broken clouds':
        weatherLabel = "hotdry"
    else: 
        weatherLabel = "warmrain"

    return weatherLabel


def sortclothes():
    getWeather()

    if getWeather() is "colddry": 
        print(top5colddry)
    elif getWeather() is "coldrain": 
        print(top5coldrain)
    elif getWeather() is "coldsnow": 
        print(top5coldsnow)
    elif getWeather() is "chillydry": 
        print(top5chillydry)
    elif getWeather() is "chillyrain": 
        print(top5chillyrain)
    elif getWeather() is "chillysnow": 
        print(top5chillysnow)
    elif getWeather() is "warmdry": 
        print(top5warmdry)
    elif getWeather() is "warmrain": 
        print(top5warmrain)
    elif getWeather() is "hotdry": 
        print(top5hotdry) 
    elif getWeather() is "hotrain": 
        print(top5warmrain)

#load the json file 
with open('nordstrom.json')  as f: 
    nordsdata = json.load(f) 
df = pd.DataFrame(nordsdata[0]['clothing'])

#convert discount_percent into an int 
#df['discount_percent'] = df['discount_percent'].astype(int)

## FIGURING OUT WEIGHTED RATING
No_Reviews = df['reviews']
Rating = df['rating']
#MeanReview = df['rating'].mean()
#minReview = ((df['reviews']).astype(int)).quantile(0.5)
df['weighted_rating'] = (0.5*Rating) + (5*(1-0.5))*(1-(np.exp((-No_Reviews)/50)))

## FIGURING OUT WEIGHTED RATING AND DISCOUNT BALANCE
weighted_rating = df['weighted_rating']
df['discount_percent'] = pd.to_numeric(df['discount_percent'],errors='coerce')
discount_percent = df['discount_percent']
p = 0.5
df['weighted_discount'] = (p*(weighted_rating)) + (5*(1-p))*(1-(np.exp(((-discount_percent)/20))))
#extract each different type of clothing from the dataset
colddry = df[df.name.str.contains('hoodie| pullover| joggers| jacket| sweatshirt',case=False)]
coldrain = df[df.name.str.contains('hoodie| pullover| joggers| jacket| sweatshirt',case=False)]
coldsnow= df[df.name.str.contains('hoodie| pullover| joggers| jacket| sweatshirt',case=False)]
chillydry= df[df.name.str.contains('hoodie| sweatshirt| vest| long sleeve| pants',case=False)]
chillyrain= df[df.name.str.contains('hoodie| sweatshirt| vest| long sleeve| pants',case=False)]
chillysnow= df[df.name.str.contains('hoodie| jacket| sweatshirt| vest| long sleeve| pants',case=False)]
warmdry= df[df.name.str.contains('tights| vest| shorts| polo| top| pants',case=False)]
warmrain = df[df.name.str.contains('tights| vest| shorts| polo| top| pants',case=False)]
hotdry= df[df.name.str.contains('tights| vest| shorts| polo| top| t-shirt',case=False)]
hotrain= df[df.name.str.contains('tights| vest| shorts| polo| top| t-shirt',case=False)]


#Sort clothes according to desired parameters
sort_colddry = colddry.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_coldrain = coldrain.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_coldsnow = coldsnow.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_chillydry = chillydry.sort_values(by= ['discount_percent','weighted_rating', 'price'], ascending = [False, False, True])
#sort_chillyrain = chillyrain.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_chillysnow = chillysnow.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_warmdry = warmdry.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_warmrain = warmrain.sort_values(by= ['discount_percent', 'weighted_rating', 'price'], ascending = [False, False, True])
sort_hotdry = hotdry.sort_values(by= ['discount_percent', 'weighted_rating','price'], ascending = [False, False, True])
sort_hotrain = hotrain.sort_values(by= ['discount_percent', 'weighted_rating','price'], ascending = [False, False, True])
sort_chillyrain = chillyrain.sort_values(by= ['weighted_discount', 'price', 'gender'], ascending = [False, True, True])

#get top 6 items per weather condition
top5colddry = sort_colddry.head(6)
top5coldrain = sort_coldrain.head(6)
top5coldsnow = sort_coldsnow.head(6)
top5chillydry = sort_chillydry.head(6)
top5chillyrain = sort_chillyrain.head(10)
top5chillysnow = sort_chillysnow.head(6)
top5warmdry = sort_warmdry.head(6)
top5warmrain = sort_warmrain.head(6)
top5hotdry = sort_hotdry.head(6)
top5warmrain = sort_hotrain.head(6)

print("The current weather condition is: " + getWeather())
sortclothes()


   