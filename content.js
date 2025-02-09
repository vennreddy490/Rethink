if (!document.getElementById("myExtensionButton")) {
    let button = document.createElement("button");
    button.id = "myExtensionButton";
    button.innerText = "Open YouTube";

    // Ensure it's positioned on the screen
    button.style.position = "fixed";
    button.style.top = "20px";
    button.style.right = "20px";
    
    // Increase visibility
    button.style.zIndex = "999999"; // Ensure it's above other elements
    button.style.background = "red"; // Ensure it's visible
    button.style.color = "white";
    button.style.padding = "10px";
    button.style.border = "2px solid white"; // Helps visibility
    button.style.fontSize = "14px";
    button.style.cursor = "pointer";

    // Ensure it's actually visible
    button.style.visibility = "visible";
    button.style.opacity = "1";
    button.style.display = "block";

    // Button action: Open YouTube
    button.addEventListener("click", function() {
        // Get the current page URL dynamically
        const currentUrl = window.location.href;

        // Data to send in the POST request
        const postDataNum = {
            num: 34  // Test value to send
        };

        const postDataText = {
            text: currentUrl  // Example string
        };

        // Send a POST request to Flask backend
        fetch("http://127.0.0.1:5000/post-test", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(postDataNum)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response:", data);
        })
        .catch(error => console.error("Error contacting backend:", error));

        // Send POST request with a string
        fetch("http://127.0.0.1:5000/post-string", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(postDataText)
        })
        .then(response => response.json())
        .then(data => {
            console.log("String (URL) Server Response:", data);
        })
        .catch(error => console.error("Error contacting backend (string):", error));

        // INSERT ALL THE JAVASCRIPT THAT YOU WANT TO RUN WHEN BUTTON IS CLICKED


        // Open YouTube in a new tab
        window.open("https://www.youtube.com", "_blank");
    });


    // INSERT ALL THE JAVASCRIPT THAT YOU WANT TO RUN WHEN THE PAGE LOADS
    // Example:
    fetch("http://127.0.0.1:5000/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data);
    })
    .catch(error => console.error("Error contacting backend:", error));


    document.body.appendChild(button);
}
