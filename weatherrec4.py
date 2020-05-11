import json 
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

##weather labels: cold, chilly, warm, hot
##precipitation labels: dry, rain, snow

def getWeather(temperature = 0, precipitation = "none"):
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
    else: 
        weatherLabel = "weathernotfound"

    return weatherLabel



def sortclothes():
    getWeather()

    if getWeather() is "colddry": 
        #print(sort_colddry[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        print(sort_colddry)
    elif getWeather() is "coldrain": 
        #print(sort_coldrain[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        print(sort_coldrain)
    elif getWeather() is "coldsnow": 
        #print(sort_coldsnow[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        print(sort_coldsnow)
    elif getWeather() is "chillydry": 
        print(sort_chillydry[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        #print(sort_chillydry)
    elif getWeather() is "chillyrain": 
        print(sort_chillyrain[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        #print(sort_chillyrain)
    elif getWeather() is "chillysnow": 
        print(sort_chillysnow[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        #print(sort_chillysnow)
    elif getWeather() is "warmdry": 
        #print(sort_warmdry[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        print(sort_warmdry)
    elif getWeather() is "warmrain": 
        #print(sort_warmrain[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
        print(sort_warmrain)
    elif getWeather() is "hotdry": 
        #print(sort_hotdry[['category','gender', 'name', 'weighted_rating', 'weighted_discount']]) 
        print(sort_hotdry)
    elif getWeather() is "hotrain": 
        print(sort_hotrain)
        #print(sort_warmrain[['category','gender', 'name', 'weighted_rating', 'weighted_discount']])
    elif getWeather() is "weathernotfound": 
        print(sort_noweather[['gender', 'category', 'weighted_discount', 'name']])

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

#sort by weighted_discount followed by price
df = df.sort_values(by = ['weighted_discount', 'price'], ascending = [False, True])

#get rid of items that have duplicate names, only keeping the first one i.e. the best of the duplicates
df = df.drop_duplicates(subset = ['name'])
#get rid of items with the word "nursing" or "maternity" in them since we dont want to recommend maternity dresses
df = df[~df.name.str.contains("nursing|maternity", case = False)]

#assign clothing categories to weather labels 
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

#noweather recommendations
# noweathermale = df[df['gender'].isin(['FEMALE'])]
# noweathermale = df.drop_duplicates(subset = ['category'])
# noweatherfemale = (df[df['gender'].isin(['MALE'])])
# noweatherfemale = df.drop_duplicates(subset = ['category'])
# sort_noweather = pd.concat([noweathermale.head(3), noweatherfemale.head(3)])


noweathermale = df.drop_duplicates(subset = ['category'])
noweathermale = df[df['gender'].isin(['MALE'])]
noweatherfemale = (df[df['gender'].isin(['FEMALE'])])
noweatherfemale = df.drop_duplicates(subset = ['category'])
sort_noweather = pd.concat([noweathermale.head(3), noweatherfemale.head(3)])

#GET 3 MALE 3 FEMALE DISTINCT ITEMS for each weather label
#COLDDRY
colddrymale = colddry[colddry['gender'].isin(['MALE'])]
colddrymale = colddrymale.drop_duplicates(subset = ['category'])
colddryfemale = (colddry[colddry['gender'].isin(['FEMALE'])])
colddryfemale = colddryfemale.drop_duplicates(subset = ['category'])
sort_colddry = pd.concat([colddrymale.head(3), colddryfemale.head(3)])

#COLDRAIN
coldrainmale = coldrain[coldrain['gender'].isin(['MALE'])]
coldrainmale = coldrainmale.drop_duplicates(subset = ['category'])
coldrainfemale = (coldrain[coldrain['gender'].isin(['FEMALE'])])
coldrainfemale = coldrainfemale.drop_duplicates(subset = ['category'])
sort_coldrain = pd.concat([coldrainmale.head(3), coldrainfemale.head(3)])

#COLDSNOW
coldsnowmale = coldsnow[coldsnow['gender'].isin(['MALE'])]
coldsnowmale = coldsnowmale.drop_duplicates(subset = ['category'])
coldsnowfemale = (coldsnow[coldsnow['gender'].isin(['FEMALE'])])
coldsnowfemale = coldsnowfemale.drop_duplicates(subset = ['category'])
sort_coldsnow = pd.concat([coldsnowmale.head(3), coldsnowfemale.head(3)])
#CHILLYDRY
chillydrymale = chillydry[chillydry['gender'].isin(['MALE'])]
chillydrymale = chillydrymale.drop_duplicates(subset = ['category'])
chillydryfemale = (chillydry[chillydry['gender'].isin(['FEMALE'])])
chillydryfemale = chillydryfemale.drop_duplicates(subset = ['category'])
sort_chillydry = pd.concat([chillydrymale.head(3), chillydryfemale.head(3)])
#Chillyrain
chillyrainmale = chillyrain[chillyrain['gender'].isin(['MALE'])]
chillyrainmale = chillyrainmale.drop_duplicates(subset = ['category'])
chillyrainfemale = (chillyrain[chillyrain['gender'].isin(['FEMALE'])])
chillyrainfemale = chillyrainfemale.drop_duplicates(subset = ['category'])
sort_chillyrain = pd.concat([chillyrainmale.head(3), chillyrainfemale.head(3)])
#chillysnow
chillysnowmale = chillysnow[chillysnow['gender'].isin(['MALE'])]
chillysnowmale = chillysnowmale.drop_duplicates(subset = ['category'])
chillysnowfemale = (chillysnow[chillysnow['gender'].isin(['FEMALE'])])
chillysnowfemale = chillysnowfemale.drop_duplicates(subset = ['category'])
sort_chillysnow = pd.concat([chillysnowmale.head(3), chillysnowfemale.head(3)])
#warmdry
warmdrymale = warmdry[warmdry['gender'].isin(['MALE'])]
warmdrymale = warmdrymale.drop_duplicates(subset = ['category'])
warmdryfemale = (warmdry[warmdry['gender'].isin(['FEMALE'])])
warmdryfemale = warmdryfemale.drop_duplicates(subset = ['category'])
sort_warmdry = pd.concat([warmdrymale.head(3), warmdryfemale.head(3)])
#warmrain
warmrainmale = warmrain[warmrain['gender'].isin(['MALE'])]
warmrainmale = warmrainmale.drop_duplicates(subset = ['category'])
warmrainfemale = (warmrain[warmrain['gender'].isin(['FEMALE'])])
warmrainfemale = warmrainfemale.drop_duplicates(subset = ['category'])
sort_warmrain = pd.concat([warmrainmale.head(3), warmrainfemale.head(3)])
#hotdry
hotdrymale = hotdry[hotdry['gender'].isin(['MALE'])]
hotdrymale = hotdrymale.drop_duplicates(subset = ['category'])
hotdryfemale = (hotdry[hotdry['gender'].isin(['FEMALE'])])
hotdryfemale = hotdryfemale.drop_duplicates(subset = ['category'])
sort_hotdry = pd.concat([hotdrymale.head(3), hotdryfemale.head(3)])
#hotrain
hotrainmale = hotrain[hotrain['gender'].isin(['MALE'])]
hotrainmale = hotrainmale.drop_duplicates(subset = ['category'])
hotrainfemale = (hotrain[hotrain['gender'].isin(['FEMALE'])])
hotrainfemale = hotrainfemale.drop_duplicates(subset = ['category'])
sort_hotrain = pd.concat([hotrainmale.head(3), hotrainfemale.head(3)])


print("The current weather condition is: " + getWeather())
sortclothes()


   