if (!document.getElementById("myExtensionButton")) {
    let logo_img = document.createElement("img")
    logo_img.style.height = "40px"
    logo_img.style.width = "40px"
    logo_img.src = chrome.runtime.getURL('/static/assets/RethinkLogo.png')

    let button = document.createElement("button");
    button.id = "myExtensionButton";
    button.appendChild(logo_img)

    // Ensure it's positioned on the screen
    button.style.position = "fixed";
    button.style.top = "100px";
    button.style.right = "10px";
    
    // Increase visibility
    button.style.zIndex = "9998";
    button.style.background = "rgba(142,29,29, 0.5)";
    button.style.padding = "6px";
    button.style.cursor = "pointer";
    button.style.borderWidth = "0px"
    button.style.borderRadius = "5px"

    // Ensure it's actually visible
    button.style.visibility = "visible";
    button.style.opacity = "1";
    button.style.display = "block";

    // Button action: Open YouTube
    button.addEventListener("click", function() {
      if (document.querySelector('.resize-drag').style.visibility == 'hidden') {
        document.querySelector('.resize-drag').style.visibility = 'visible'
    } else {
        document.querySelector('.resize-drag').style.visibility = 'hidden'
    }
    });


    // INSERT ALL THE JAVASCRIPT THAT YOU WANT TO RUN WHEN THE PAGE LOADS
    fetch("http://127.0.0.1:5000/", {
        method: "GET",
        headers: {
            //"Content-Type": "application/json"
        }
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        doc = parser.parseFromString(data, 'text/html')

        console.log("test")
        activateImages(doc)
        document.body.insertAdjacentHTML('afterbegin', doc.documentElement.innerHTML)
        loadScript(chrome.runtime.getURL('static/scripts/interact.min.js'))
        jankyWindowActivation()

        document.querySelector('.close-button').addEventListener("click", () => {
          panel = document.querySelector('.resize-drag')
          panel.top = '100px'
          panel.right = '300px'
          panel.height = '500px'
          panel.width = '550px'
          panel.style.visibility = 'hidden'
        });

        console.log(window.closePanel)

        console.log("Server Response:", data);
        
    })
    .catch(error => console.error("Error contacting backend:", error));

    // CODE THAT POSTS URL TO FLASK /APP ROUTE:
    fetch("http://127.0.0.1:5000/app", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ main_url: window.location.href }) // Sends current page URL
  })
  .then(response => response.text())
  .then(data => {
      console.log("Response from Flask:", data);
  })
  .catch(error => console.error("Error sending URL to Flask:", error));
  
  
    // CODE THAT ADDS BUTTON TO DOM:
    document.body.appendChild(button);
}

function loadScript(src, defer = false) {
    const script = document.createElement('script');
    script.src = src;
    script.type = 'text/javascript';
    if (defer) script.defer = true;
    document.head.appendChild(script);
}

function activateImages(html) {
    const images = html.querySelectorAll('img');
    images.forEach((img) => {
        console.log('first', img.src)
        img.src = chrome.runtime.getURL(img.src.substring(img.src.indexOf("/static/") + 1));
        console.log('second', img.src)
    })
}

function jankyWindowActivation() {
    interact('.resize-drag')
  .resizable({
    // resize from all edges and corners
    edges: { left: true, right: true, bottom: true, top: true },
    margin: 5,
    ignoreFrom: '.ignore-resize',
    listeners: {
      move (event) {
        var target = event.target
        var x = (parseFloat(target.getAttribute('data-x')) || 0)
        var y = (parseFloat(target.getAttribute('data-y')) || 0)

        // update the element's style
        target.style.width = event.rect.width + 'px'
        target.style.height = event.rect.height + 'px'

        // translate when resizing from top or left edges
        x += event.deltaRect.left
        y += event.deltaRect.top

        target.style.transform = 'translate(' + x + 'px,' + y + 'px)'

        target.setAttribute('data-x', x)
        target.setAttribute('data-y', y)
      }
    },
    modifiers: [
      // keep the edges inside the parent
      interact.modifiers.restrictEdges({
        outer: 'window'
      }),

      // minimum size
      interact.modifiers.restrictSize({
        min: { width: 100, height: 50 }
      })
    ],

    inertia: true
  })
  .draggable({
    listeners: { move: window.dragMoveListener },
    inertia: true,
    ignoreFrom: '.ignore-drag',
    cursorChecker () {
      return 'move'
    },
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: 'window',
        endOnly: true
      })
    ]
  })

  function dragMoveListener (event) {
    var target = event.target
    // keep the dragged position in the data-x/data-y attributes
    var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
    var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy
  
    // translate the element
    target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'
  
    // update the posiion attributes
    target.setAttribute('data-x', x)
    target.setAttribute('data-y', y)
  }
  
  // this function is used later in the resizing and gesture demos
  window.dragMoveListener = dragMoveListener
}

function activateCloseButton() {
  window.closePanel = closePanel
  document.querySelector('.close-button').onClick = closePanel
}

function closePanel() {
  panel = document.querySelector('.resize-drag')
  panel.style.visibility = 'hidden'
  panel.top = '500px'
  panel.right = '50px'
  panel.height = '500px'
  panel.width = '550px'
}