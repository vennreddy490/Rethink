chrome.webNavigation.onCompleted.addListener((details) => {
  // Ensure it's the main frame (not an iframe or embedded script)
  if (details.frameId === 0) {
      console.log(`Main page loaded: ${details.url}`);

      // Data to send in the POST request
      const postData = {
          site: details.url  // Send only the main page URL
      };

      // Send POST request to Flask backend
      fetch("http://127.0.0.1:5000/find-source", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(postData)
      })
      .then(response => response.json())
      .then(data => {
          console.log("Background Script - Server Response:", data);
      })
      .catch(error => console.error("Error in background script request:", error));
  }
}, { url: [{ schemes: ["http", "https"] }] });

// chrome.webNavigation.onCompleted.addListener((details) => { 
//   chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//     if (tabs && tabs.length > 0) {
//       const activeTab = tabs[0];
//       console.log("Active tab details:", activeTab);
//       console.log("Active tab URL:", activeTab.url);
      
//       if (details.url) {
//         console.log("Website loaded...");
//         // Create an object with the activeTab URL.
//         const dataToSend = { url: activeTab.url };
//         console.log("Hello World:", dataToSend.url)
//         console.log(typeof activeTab.url)
//         console.log(typeof dataToSend.url)
//         payload = dataToSend
//         fetch("http://127.0.0.1:5000/find-source", { 
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json"
//           },
//           body: JSON.stringify(payload)
          
//         })
//         .then(response => response.json())
//         .then(payload => { 
//             console.log("Response data:", payload);

//         })
//         .catch(error => console.error("Error in script", error));
//       }
    
//     } else {
//       console.log("No active tab found.");
//     }
//   });
// });




// chrome.webNavigation.onCompleted.addListener((details) => { 

//   chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//     if (tabs && tabs.length > 0) {
//       const activeTab = tabs[0];
//       console.log("Active tab details:", activeTab);
//       console.log(activeTab.url)
//       if (details.url) {
//         console.log("Website loaded...")
//         // console.log(details.url)
//         const payload = {url: activeTab.url}; 

//         data = activeTab.url
//         fetch("http://127.0.0.1:5000/find-source", { 
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json"
        
//           },
//           body: JSON.stringify(payload)
//         })
//         .then(response => response.json())
//         .then(payload => { 
//             console.log("This is the data:", payload)
//         })
//         .catch(error => console.error("error in script", error))
//       }
    
//     } else {
//       console.log("No active tab found.");
//     }
//   });
// })


///////////////////////////////////////
  
 
  // if (details.url) {
  //   console.log("Website loaded...")
  //   // console.log(details.url)
  //   fetch("http://127.0.0.1:5000/find-source", { 
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json"
    
  //     },
  //     body: JSON.stringify(details)
  //   })
  //   .then(response => response.json())
  //   .then(data => { 
  //       console.log(data)
  //   })
  //   .catch(error => console.error("error in script", error))
  // }






// chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
//     // Check that the tab finished loading and is active.
//     if (changeInfo.status === 'complete' && tab.active) {
//       const activeUrl = tab.url;
//       console.log("Active tab URL:", activeUrl);
  
//       // Prepare the data payload.
//       const data = { url: activeUrl };
  
//       // Send a POST request to the Flask backend.
//       fetch('http://localhost:5000/app', {  // Update URL as needed.
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//       })
//         .then(response => {
//           if (!response.ok) {
//             throw new Error(`Server error: ${response.statusText}`);
//           }
//           return response.json();
//         })
//         .then(responseData => {
//           console.log('Response from backend:', responseData);
//           // Optionally, you can perform further actions based on the response.
//         })
      
//     }
//   });
  