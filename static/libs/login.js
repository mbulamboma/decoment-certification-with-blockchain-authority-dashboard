// Get the form element
const form = document.getElementById('postLoginForm');
const loading = document.getElementById('loading');

// Add event listener for form submission
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    var email = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    loading.classList.remove('d-none');

    var data = {
        "email": email,
        "password": password
    };

    // Send the POST request
    fetch('/authenticate', {
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
            document.getElementById("errorMessage").textContent = "An error occured, retry later ..."
        }
    }) // Assuming the response is in JSON format
    .then(data => {
        loading.classList.add('d-none');
        if(data.loggedin == true){
            // save token
            
            localStorage.setItem('token', data.token);
             //The user loggedIn successfully
             var currentUrl = window.location.href;
             var nextParamRegex = /[\?&]next=([^&]+)/;
             var match = currentUrl.match(nextParamRegex);
             if (match) {
                 // If the "next" parameter exists, extract the next URL
                 var nextUrl = decodeURIComponent(match[1]); 
                 window.location.href = nextUrl;
             } else {
                 // If the "next" parameter is not found, display a message or perform some other action
                 console.log("Next URL not found in the current URL.");
                 window.location="/cpanel";
             }
        }else{ 
            if (data.message) { 
                document.getElementById("errorMessage").textContent = data.message;
            }
            else{
                document.getElementById("errorMessage").textContent = "The server returned nothing, retry please";
            } 
        }
        console.log(data);
    })
    .catch(error => { 
        // an error occured
        loading.classList.add('d-none');
        console.error('Error:', error);
        document.getElementById("errorMessage").textContent = "An error occured, retry later ..."
    });
});