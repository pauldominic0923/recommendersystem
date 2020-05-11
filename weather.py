import requests
city = input('Enter City Name: ')
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=3739750b9f8a52c079de7d8292030d35&units=metric'.format(city)
res = requests.get(url)
data = res.json()
print(data)

temp = data['main']['temp']
windspeed = data['wind']['speed']
precipitation = data['weather'][0]['precipitation']

print('Temperature: ', temp)
print('Wind Speed: {}'.format(wind_speed))
print('Precipitation: {}'.format(precipitation))
with open('res.json', 'w') as f:
    json.dump(data, f)