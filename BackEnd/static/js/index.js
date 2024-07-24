

document.getElementById('logout').addEventListener('click', function() {
    fetch("do_logout", {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,  // Use the token defined in the template
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // Check if the response contains a redirect URL
                if (data.redirect) {
                    window.location.href = data.redirect;  // Redirect to login page
                } else {
                    throw new Error(data.Error || 'Network response was not ok');
                }
            });
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // This will only execute if the logout is successful without errors
        window.location.href = "login";  // Redirect to login page
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally redirect to login if there's a network error
        window.location.href = "login";  // Redirect to login page
    });
});

