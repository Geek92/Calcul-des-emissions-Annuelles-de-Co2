fetch('http://localhost/get_travel_ghg_emission')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return response.json();
    })
    .then(data => {
        console.log('Data received from backend:', data);
    })

    .catch(error => {
        console.error('an error occured during data acquisition:', error);
    });