    // // GET
    fetch('/hello')
        .then(function (response) {
            return response.text();
        }).then(function (text) {

            // Print the greeting as text
            console.log('GET response text:');
            console.log(text);
        });

    // Send the same request
    fetch('/hello')
        .then(function (response) {

            // But parse it as JSON this time
            return response.json();
        })
        .then(function (json) {

            // Do anything with it!
            console.log('GET response as JSON:');
            console.log(json);
        })

    // POST
    fetch('/hello', {

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify({
            "greeting": "Hello from the browser!"
        })
    }).then(function (response) {
        return response.text();
    }).then(function (text) {

        console.log('POST response: ');

        // Should be 'OK' if everything was successful
        console.log(text);
    });