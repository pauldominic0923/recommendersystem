var city = "Miami"

document.getElementById("location").innerHTML = city;

  fetch('/cityWeather', {
    method: 'POST',
    body: JSON.stringify({
      "city": city
    })
  }).then(function (response) {
    return response.text();
  }).then(function (text) {
    var weatherData = JSON.parse(text)
    var temperature = weatherData.main.temp;
    var description = weatherData.weather[0].main;
    document.getElementById("temperature").innerHTML = Math.round(temperature) + "&#8451";
    console.log('Temperature: ');
    console.log(temperature);
    console.log('Wind Speed: ');
    console.log(weatherData.wind.speed);
    console.log('Main: ');
    console.log(description);
    console.log('Description: ');
    console.log(weatherData.weather[0].description);
    document.getElementById("svg-img").src = "static/img/" + weatherData.weather[0].icon + ".svg";
    console.log('Icon: ');
    console.log(weatherData.weather[0].icon);
    sendDataToFlask(temperature, description);
  });

function sendDataToFlask (temperature, description) {
  fetch('/recommendation', {
        method: 'POST',
        body: JSON.stringify({
          "temperature": temperature,
          "precipitation": description
        })
      }).then(function (response) {
        return response.text();
      }).then(function (text) {
        var recommendationData = JSON.parse(text);
        console.log(recommendationData);

        for (var items = 0; items < Object.keys(recommendationData).length; items++) {
          document.getElementById("img"+items).src = recommendationData[items].img;
          document.getElementById("name"+items).innerHTML = recommendationData[items].name + "<br>($" + recommendationData[items].price + ")";
          document.getElementById("name"+items).href = recommendationData[items].link;
        }
      });
} 