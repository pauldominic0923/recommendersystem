var geocoder;

initialize()
if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(successFunction, errorFunction);
}
//Get the latitude and the longitude;
function successFunction(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    codeLatLng(lat, lng)
}

function errorFunction(){
	alert("Geocoder failed");
  sendDataToFlask("none", "none");
}

function initialize() {
	geocoder = new google.maps.Geocoder();
}

function codeLatLng(lat, lng) {

var latlng = new google.maps.LatLng(lat, lng);
  geocoder.geocode({'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
    console.log(results)
      if (results[1]) {
      //formatted address
      // alert(results[0].formatted_address)
      //find country name
      for (var i=0; i<results[0].address_components.length; i++) {
        for (var b=0;b<results[0].address_components[i].types.length;b++) {
          if (results[0].address_components[i].types[b] == "locality") {
            city= results[0].address_components[i];
            break;
          }
        }
      }
      //city name
      document.getElementById("location").innerHTML = city.long_name;

      fetch('/cityWeather', {
        method: 'POST',
        body: JSON.stringify({
          "city": city.long_name
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

      } else {
        alert("No results found");
      }
    } else {
      alert("Geocoder failed due to: " + status);
    }
  });
}

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

