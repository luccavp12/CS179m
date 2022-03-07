// This is the change list json object to be filled and sent to the backend
var changeList = new Object();

// Getting all of the container div elements
const containerButtonArr = document.getElementsByClassName("containerButtonContainer");

// Getting the div element of the "begin balancing" submit button
const beginBalanceButton = document.getElementById("inputSubmitButton");

// Checking for when someone clicks on either of the mode changing buttons
// Checking if someone clicks on the button and then forwarding it to next and Submit
beginBalanceButton.addEventListener("click", nextAndSubmit);

function nextAndSubmit(ev) {
    ev.preventDefault();

    // Goes through all of the containers and formats them in a JSON object for algorithm
    for (let i = 0; i < containerButtonArr.length; i++) {
        var containerPosition = containerButtonArr[i].children[0].id;
        var containerWeight = containerButtonArr[i].children[0].children[1].textContent;
        var containerDescription = containerButtonArr[i].children[0].children[2].textContent;

        var obj = new Object();
        // obj.position = containerPosition;
        obj.weight = containerWeight.slice(1, -1);
        obj.description = containerDescription;

        changeList[containerPosition] = obj;        
    }

    // The changeList is now formatted and able to be sent to the backend to balance!
    console.log(changeList);
    var changeListJson = JSON.stringify(changeList);
    // console.log(changeListJson);

    fetch(urlForAlgo, {
        method: 'POST',
        credentials: "include",
        body: changeListJson,
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function(response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function(data) {
          console.log(data);
          displayBalancing(data);
        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });    
}

var currentStep = 1;

function displayBalancing(data) {
    console.log("Inside displayBalancing");
    
    // We need to disable the submit div so we can see the containers
    const beginBalanceButton = document.getElementById("informationInputContainer");
    beginBalanceButton.style.display = "none";
    
    // GO THROUGH every item in the returned json and show the steps of balancing!

    const nextButton = document.getElementById("nextButton");
    var currentStep = 1;
    nextButton.addEventListener("click", nextBalanceOperation);
    nextButton.data = data;

    highlightCurrentOperation(data[1]["origin"], data[1]["destination"]);

    console.log(data);
    // for (var element in data) {
    //     console.log(data[element]["origin"]);
    //     console.log(data[element]["destination"]);
    // }
}

function nextBalanceOperation(evt) {
    currentStep = currentStep + 1;

    // Get the data object
    data = evt.currentTarget.data;
    
    // Everytime we click "next", we need to clear the previous operation
    var prevOrigin = data[currentStep - 1]["origin"];
    var prevDestination = data[currentStep - 1]["destination"];
    
    // Get the previous origin and destination container
    const prevOriginContainer = document.getElementById(prevOrigin);
    const prevDestinationContainer = document.getElementById(prevDestination);

    // Grab the weight and description so that we can swap them after the move is done
    prevOriginContainerWeight = prevOriginContainer.children[1].textContent;
    prevOriginContainerDescription = prevOriginContainer.children[2].textContent;
    
    prevDestinationContainerWeight = prevDestinationContainer.children[1].textContent;
    prevDestinationContainerDescription = prevDestinationContainer.children[2].textContent;

    // Swap the weights and descriptions 
    prevDestinationContainer.children[1].textContent = prevOriginContainerWeight;
    prevDestinationContainer.children[2].textContent = prevOriginContainerDescription;

    prevOriginContainer.children[1].textContent = prevDestinationContainerWeight;
    prevOriginContainer.children[2].textContent = prevDestinationContainerDescription;

    // Finalize the previous operation by turning it back to white
    prevOriginContainer.style.backgroundColor = "white";
    prevDestinationContainer.style.backgroundColor = "white";

    // Get the next operation and pass it into the highlight function
    // In a try block because it will eventually reach the end of the data object
    try {
        var origin = data[currentStep]["origin"];
        var destination = data[currentStep]["destination"];
    
        highlightCurrentOperation(origin, destination);
    } catch (error) {
        // We reached the end and can now procede in our direction
        console.log("Reached end of the data object");

        // TODO IMPLEMENT THE NEXT STEP IN THE PROCESS
    }
}

function highlightCurrentOperation(origin, destination) {
    const originContainer = document.getElementById(origin);
    const destinationContainer = document.getElementById(destination);

    originContainer.style.backgroundColor = "green";
    destinationContainer.style.backgroundColor = "red";
}