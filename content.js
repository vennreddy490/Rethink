if (!document.getElementById("myExtensionButton")) {
    let button = document.createElement("button");
    button.id = "myExtensionButton";
    button.innerText = "Open YouTube";

    // Ensure it's positioned on the screen
    button.style.position = "fixed";
    button.style.top = "20px";
    button.style.right = "20px";
    
    // Increase visibility
    button.style.zIndex = "9998"; // Ensure it's above other elements
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
        console.log('fdjskfjdslkfjlsdk')
        document.querySelector('.resize-drag').style.visibility = 'visible'
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
        console.log("Server Response:", data);
        
    })
    .catch(error => console.error("Error contacting backend:", error));

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