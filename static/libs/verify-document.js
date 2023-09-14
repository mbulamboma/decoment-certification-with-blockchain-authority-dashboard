// Get the form element
const form = window.document.getElementById('certifyForm');
const loading = window.document.getElementById('loading');
const formButton = window.document.getElementById('formButton');
const responseContainer = window.document.getElementById('response-content'); 
 
form.addEventListener('submit', function (event) {
    event.preventDefault();  
    
    formButton.classList.add('disabled');
    loading.classList.remove('d-none');

    //get data
    var hashtext = window.document.getElementById("hashtext").value; 

    var data = {
        "hashtext": hashtext
    };

    // Send the POST request
    fetch('/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            responseContainer.innerHTML = "An error occured, retry later ..."
        }
    }) // Assuming the response is in JSON format
    .then(data => {
        console.log(data)
        loading.classList.add('d-none');
        responseContainer.innerHTML = data['message']
        formButton.classList.remove('disabled');
        console.log(data);
    })
    .catch(error => { 
        // an error occured
        
        formButton.classList.remove('disabled');
        loading.classList.add('d-none');
        console.error('Error:', error);
        responseContainer.innerHTML = "An error occured, retry later ..."
    });
});