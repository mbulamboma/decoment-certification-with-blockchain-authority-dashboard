// Get the form element
const form = window.document.getElementById('certifyForm');
const loading = window.document.getElementById('loading');
const formButton = window.document.getElementById('formButton');
 
form.addEventListener('submit', function (event) {
    event.preventDefault();  
    
    formButton.classList.add('disabled');
    loading.classList.remove('d-none');

    //get data
    var certId = window.document.getElementById("certId").value; 

    var data = {
        "phone": certId
    };

    // Send the POST request
    fetch('/doc-certify-now', {
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
            window.document.getElementById("errorMessage").textContent = "An error occured, retry later ..."
        }
    }) // Assuming the response is in JSON format
    .then(data => {
        loading.classList.add('d-none');
        if(data.success == true){    
            window.location.href = data.next; 
        }else{ 
            if (data.message) { 
                window.document.getElementById("errorMessage").textContent = data.message;
            }
            else{
                window.document.getElementById("errorMessage").textContent = "The server returned nothing, retry please";
            } 
        
            formButton.classList.remove('disabled');
            loading.classList.add('d-none');
        }
        console.log(data);
    })
    .catch(error => { 
        // an error occured
        
        formButton.classList.remove('disabled');
        loading.classList.add('d-none');
        console.error('Error:', error);
        window.document.getElementById("errorMessage").textContent = "An error occured, retry later ..."
    });
});