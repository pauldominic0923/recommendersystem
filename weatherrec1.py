import json 
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

##weather labels: cold, chilly, warm, hot
##precipitation labels: dry, rain, snow

def getWeather(temperature = 20, precipitation = 'clear sky'):
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
    elif temperature >=20 and precipitation == 'clear sky' or precipitation == 'few clouds' or precipitation == 'scattered clouds' or precipitation == 'broken clouds':
        weatherLabel = "hotdry"
    else: 
        weatherLabel = "warmrain"

    return weatherLabel


def sortclothes():
    getWeather()

    if getWeather() is "colddry": 
        print(sort_colddry1)
    elif getWeather() is "coldrain": 
        print(sort_coldrain1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "coldsnow": 
        print(sort_coldsnow1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "chillydry": 
        print(sort_chillydry1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "chillyrain": 
        print(sort_chillyrain1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "chillysnow": 
        print(sort_chillysnow1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "warmdry": 
        print(sort_warmdry1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "warmrain": 
        print(sort_warmrain1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])
    elif getWeather() is "hotdry": 
        print(sort_hotdry1) 
    elif getWeather() is "hotrain": 
        print(sort_warmrain1[['name','gender', 'product_id', 'discount_percent', 'rating', 'reviews']])

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

p = 0.7
df['weighted_discount'] = (p*(weighted_rating)) + (5*(1-p))*(1-(np.exp(((-discount_percent)/20))))
#extract each different type of clothing from the dataset
colddry = df[df.category.str.contains("blazers|coats|pants|jeans|sweaters|hoodies",case=False)]
coldrain = df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
coldsnow= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
chillydry= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
chillyrain= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
chillysnow= df[df.category.str.contains('blazers|coats|pants |jeans|sweaters|hoodies',case=False)]
warmdry= df[df.category.str.contains('shorts|polo|jeans| tank| t-shirt| dress shirts',case=False)]
warmrain = df[df.category.str.contains('shorts|polo|jeans| tank| t-shirt|dress shirts',case=False)]
hotdry= df[df.category.str.contains('shorts|polo|jeans|tank|shirts',case=False)]
hotrain= df[df.category.str.contains('shorts|polo|jeans|tank|shirts',case=False)]


#Sort clothes according to desired parameters
sort_colddry = colddry.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_coldrain = coldrain.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_coldsnow = coldsnow.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_chillydry = chillydry.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_chillyrain = chillyrain.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_chillysnow = chillysnow.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_warmdry = warmdry.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_warmrain = warmrain.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_hotdry = hotdry.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])
sort_hotrain = hotrain.sort_values(by= ['weighted_discount', 'price'], ascending = [False, True])


#Get rid of duplicate items 
sort_colddry = sort_colddry.drop_duplicates(subset = ['name'])
sort_coldrain = sort_coldrain.drop_duplicates(subset = ['name'])
sort_coldsnow = sort_coldsnow.drop_duplicates(subset = ['name'])
sort_chillydry = chillydry.drop_duplicates(subset = ['name'])
sort_chillyrain = sort_chillyrain.drop_duplicates(subset = ['name'])
sort_chillysnow = sort_chillysnow.drop_duplicates(subset = ['name'])
sort_warmdry = sort_warmdry.drop_duplicates(subset = ['name'])
sort_warmrain = sort_warmrain.drop_duplicates(subset = ['name'])
sort_hotdry = sort_hotdry.drop_duplicates(subset = ['name'])
sort_hotrain = sort_hotrain.drop_duplicates(subset = ['name'])



#GET 3 MALE 3 FEMALE
colddrymale = (sort_colddry[sort_colddry['gender'].isin(['MALE'])]).head(10)
colddryfemale = (sort_colddry[sort_colddry['gender'].isin(['FEMALE'])]).head(10)
sort_colddry1 = pd.concat([colddrymale, colddryfemale])

coldrainmale = (sort_coldrain[sort_coldrain['gender'].isin(['MALE'])]).head(10)
coldrainfemale = (sort_coldrain[sort_coldrain['gender'].isin(['FEMALE'])]).head(10)
sort_coldrain1 = pd.concat([coldrainmale, coldrainfemale])

coldsnowmale = (sort_coldsnow[sort_coldsnow['gender'].isin(['MALE'])]).head(10)
coldsnowfemale = (sort_coldsnow[sort_coldsnow['gender'].isin(['FEMALE'])]).head(10)
sort_coldsnow1 = pd.concat([coldsnowmale, coldsnowfemale])

chillydrymale = (sort_chillydry[sort_chillydry['gender'].isin(['MALE'])]).head(10)
chillydryfemale = (sort_chillydry[sort_chillydry['gender'].isin(['FEMALE'])]).head(10)
sort_chillydry1 = pd.concat([chillydrymale, chillydryfemale])

chillyrainmale = (sort_chillyrain[sort_chillyrain['gender'].isin(['MALE'])]).head(10)
chillyrainfemale = (sort_chillyrain[sort_chillyrain['gender'].isin(['FEMALE'])]).head(10)
sort_chillyrain1 = pd.concat([chillyrainmale, chillyrainfemale])

chillysnowmale = (sort_chillysnow[sort_chillysnow['gender'].isin(['MALE'])]).head(10)
chillysnowfemale = (sort_chillysnow[sort_chillysnow['gender'].isin(['FEMALE'])]).head(10)
sort_chillysnow1 = pd.concat([chillysnowmale, chillysnowmale])

warmdrymale = (sort_warmdry[sort_warmdry['gender'].isin(['MALE'])]).head(10)
warmdryfemale = (sort_warmdry[sort_warmdry['gender'].isin(['FEMALE'])]).head(10)
sort_warmdry1 = pd.concat([warmdrymale, warmdryfemale])

warmrainmale = (sort_warmrain[sort_warmrain['gender'].isin(['MALE'])]).head(10)
warmrainfemale = (sort_warmrain[sort_warmrain['gender'].isin(['FEMALE'])]).head(10)
sort_warmrain1 = pd.concat([warmrainmale, warmrainfemale])

hotdrymale = (sort_hotdry[sort_hotdry['gender'].isin(['MALE'])]).head(10)
hotdryfemale = (sort_hotdry[sort_hotdry['gender'].isin(['FEMALE'])]).head(10)
sort_hotdry1 = pd.concat([hotdrymale, hotdryfemale])

hotrainmale = (sort_hotrain[sort_hotrain['gender'].isin(['MALE'])]).head(10)
hotrainfemale = (sort_hotrain[sort_hotrain['gender'].isin(['FEMALE'])]).head(10)
sort_hotrain1 = pd.concat([hotrainmale, hotrainfemale])


#get top 6 items per weather condition
# top5colddry = sort_colddry1
# top5coldrain = sort_coldrain1
# top5coldsnow = sort_coldsnow1
# top5chillydry = sort_chillydry1
# top5chillyrain = sort_chillyrain1
# top5chillysnow = sort_chillysnow1
# top5warmdry = sort_warmdry1
# top5warmrain = sort_warmrain
# top5hotdry = sort_hotdry1
# top5warmrain = sort_hotrain1

print("The current weather condition is: " + getWeather())
sortclothes()


   