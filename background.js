chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status == 'complete' && tab.active) { 
        const activeURL = tab.url; 

        console.log(activeURL); 

        const data = {url: activeURL}; 

        fetch('http://localhost:5000/backend/find_source', { 
            method: "POST", 
            headers: { 
                'Content-Type': 'application/json'

            }, 
            body: JSON.stringify(data)
        })

        .then(response => { 
            if (!response.ok) { 
                throw new Error(`Server error ${response.statusText}`);
            }
            return response.json();
        })
        .then(responseData => { 
            console.log('Response:', responseData)
        })
        .catch(error => console.error('Error in sending URL'))
    }
} )