// This is the change list json object to be filled and sent to the backend
var changeList = new Object();
// Position list will be a list of strings that have the IDs of all the containers that are being loaded/unloaded
var positionList = [];
// loadUnloadBool will be an adjacent list of whether or not the container selected is for loading or unloading
var loadUnloadBool = [];

// SelectedMode = 0 : When no mode has been selected
// SelectedMode = 1 : When loading mode has been selected
// SelectedMode = 2 : When unloading mode has been selected
var selectedMode = 0;

// Getting the div elements
const loadingButton = document.getElementById("loadingButton");
const unloadingButton = document.getElementById("unloadingButton");

// Checking for when someone clicks on either of the mode changing buttons
loadingButton.addEventListener("click", modeChange);
unloadingButton.addEventListener("click", modeChange);

// Handles the mode change by checking what the value was before, and changes it appropriately
function modeChange() {
    console.log(this.id);
    if (this.id == "loadingButton") {
        if (selectedMode == 0) {
            selectedMode = 1;
            this.style.backgroundColor = "green";
        }
        else if (selectedMode == 2) {
            selectedMode = 1;
            unloadingButton.style.backgroundColor = "white";
            this.style.backgroundColor = "green";
        }
        else if (selectedMode == 1) {
            selectedMode = 0;
            this.style.backgroundColor = "white";
        }
    }
    else if (this.id == "unloadingButton") {
        if (selectedMode == 0) {
            selectedMode = 2;
            this.style.backgroundColor = "green";
        }
        else if (selectedMode == 1) {
            selectedMode = 2;
            loadingButton.style.backgroundColor = "white";
            this.style.backgroundColor = "green";
        }
        else if (selectedMode == 2) {
            selectedMode = 0;
            this.style.backgroundColor = "white";
        }
    }
}

// Getting all of the container div elements
const containerButtonArr = document.getElementsByClassName("containerButtonContainer");

// Loop through the list of all container buttons, and set event listeners on all of container buttons
for (var i = 0; i < containerButtonArr.length; i++) {
    containerButtonArr[i].addEventListener('click', containerSelection);
    // console.log(containerButtonArr[i].children[0].id);
}

// Event listener function for container button click
function containerSelection() {
    // We can now access the unique ID, which in turn is the position
    // console.log(this.firstElementChild.id);

    // We now have the description of the container that was clicked
    // the first children set is a single containerButton, the second children are the <p> tag values
    var containerPosition = this.children[0].id;
    var containerWeight = this.children[0].children[1].textContent;
    var containerDescription = this.children[0].children[2].textContent;
    console.log(containerPosition);
    console.log(containerWeight);
    console.log(containerDescription);
    
    // If a container button is clicked AND the user is in loading mode
    if (selectedMode == 1) {
        // if the container button that is clicked is the proper button and has no container in the location
        if (containerDescription == "UNUSED") {
            // Take the container information and send it to the Changes.json

            // Check if the button has been clicked or not
            // If it hasn't been clicked, change it to blue (selected)
            // If it has been clicked, change it back to white (unselected)
            if (this.children[0].style.backgroundColor == "blue") {
                this.children[0].style.backgroundColor = "white";

                // Gets the index of the LOADED container in the position list array
                removeIndex = positionList.indexOf(containerPosition);
                // Removes the container that was deselected in the UI
                positionList.splice(removeIndex, 1);
                // The corresponding value in the list of load/unload is also removed to stay consistent
                loadUnloadBool.splice(removeIndex, 1);

                console.log(positionList);
                console.log(loadUnloadBool);
            }
            else {
                this.children[0].style.backgroundColor = "blue";

                // Appending the position to the list of containers to be changed
                positionList.push(containerPosition);
                // Appending the corresponding mode value (1 for being loaded)
                loadUnloadBool.push(selectedMode)
                
                console.log(positionList);
                console.log(loadUnloadBool);
            }
        }
    }
    // If a container button is clicked AND the user is in unloading mode
    else if (selectedMode == 2) {
        // if the container button that is clicked is the proper button and a container in the location
        if (containerDescription != "NAN" && containerDescription != "UNUSED") {
            // Take the container information and send it to the Changes.json
            console.log("Can be bundled and sent to json");

            // Check if the button has been clicked or not
            // If it hasn't been clicked, change it to pink (selected)
            // If it has been clicked, change it back to white (unselected)
            if (this.children[0].style.backgroundColor == "pink") {
                this.children[0].style.backgroundColor = "white";

                // Gets the index of the UNLOADED container in the position list array
                removeIndex = positionList.indexOf(containerPosition);
                // Removes the container that was deselected in the UI
                positionList.splice(removeIndex, 1);
                // The corresponding value in the list of load/unload is also removed to stay consistent
                loadUnloadBool.splice(removeIndex, 1);

                console.log(positionList);
                console.log(loadUnloadBool);
            }
            else {
                this.children[0].style.backgroundColor = "pink";

                // Appending the position to the list of containers to be changed
                positionList.push(containerPosition);
                // Appending the corresponding mode value (2 for being unloaded)
                loadUnloadBool.push(selectedMode);

                console.log(positionList);
                console.log(loadUnloadBool);
            }
            // TODO: Need to at more functionality if a container is selected to be unloaded, and then loaded into
            // This will involve making it a new color, or have a mix of both colors, and then being able to be removed one at a time
            // if selected or unselected.
        }
    }
}

// Getting the div element
// const finishButton = document.getElementById("finishButton");
const finishButton = document.getElementById("finishSubmissionForm");

// Checking for when someone clicks on either of the mode changing buttons
finishButton.addEventListener("submit", finishAndSubmit);

function finishAndSubmit(ev) {
    ev.preventDefault();

    if (positionList.length == 0) {
        console.log("No changes were made to the manifest!");
    }

    changeList["changes"] = new Object();
    changeList["manifest"] = new Object();

    for (let i = 0; i < positionList.length; i++) {
        for (let j = 0; j < containerButtonArr.length; j++) {
            // Trying to retrieve all the information about the container being changed
            // if the current container to be changed is found in the full list of containers (with container details)
            var containerPosition = containerButtonArr[j].children[0].id;
            var containerWeight = containerButtonArr[j].children[0].children[1].textContent;
            var containerDescription = containerButtonArr[j].children[0].children[2].textContent;

            // We check if the container is the one that we need to add to 
            if (positionList[i] == containerButtonArr[j].children[0].id) {
                var obj = new Object();
                // obj.position = containerPosition;
                obj.weight = containerWeight.slice(1, -1);
                obj.description = containerDescription;
                obj.loadUnload = loadUnloadBool[i];

                changeList["changes"][containerPosition] = obj;
                
                console.log(obj);
            }
            var objMan = new Object();
            // obj.position = containerPosition;
            objMan.weight = containerWeight.slice(1, -1);
            objMan.description = containerDescription;

            changeList["manifest"][containerPosition] = objMan
        }
    }

    console.log("Change List with manifest and changes:");
    console.log(changeList);
    var changeListJson = JSON.stringify(changeList);
    console.log(changeListJson);

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
          console.log("Hello there!");
          displayChanges(data);
        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });    
}

var currentStep = 1;

function displayChanges(data) {
    console.log("Inside displayChanges");
    console.log(data);

    // First we have to clear the table and make it all unselected
    for (var i = 0; i < containerButtonArr.length; i++) {
        containerButtonArr[i].children[0].style.backgroundColor = "white";
        // console.log(containerButtonArr[i].children[0].id);
    }

    // Need to make the loading and unloading div disappear
    modeButtonContainer = document.getElementById("modeButtonContainer");
    modeButtonContainer.style.display = "none";

    // Need to remove the submit button and create the Next button
    const finishButton = document.getElementById("finishButton");
    finishButton.style.display = "none";
    const nextButton = document.getElementById("nextButton");
    nextButton.style.display = "flex";
    
    // GO THROUGH every item in the returned json and show the steps of balancing!
    var currentStep = 1;
    nextButton.addEventListener("click", nextOperation);
    nextButton.data = data;

    // TODO: HOW TO HANDLE THE NEW JSON AS THERE ARE DIFFERENT CONDITIONS (ORIGIN/DESTINATION BEING GONE)
    // Now based on what the condition is, we will go to seperate functions
    if (data[1]["condition"] == "0") {
        highlightCurrentOperation(data[1]["origin"], data[1]["destination"]);
    }
    else if (data[1]["condition"] == "1") {
        highlightCurrentLoad(data[1]["destination"]);
    }
    else if (data[1]["condition"] == "2") {
        highlightCurrentUnload(data[1]["destination"]);
    }
}

function nextOperation(evt) {
    currentStep = currentStep + 1;
    prevStep = currentStep - 1;
    console.log(currentStep);
    console.log(prevStep);

    // Get the data object
    data = evt.currentTarget.data;
    
    // Every time we click "next", we need to clear the previous operation
    var prevOrigin = data[prevStep]["origin"];
    var prevDestination = data[prevStep]["destination"];

    // If the last move was just a swap
    if (data[prevStep]["condition"] == "0") {
        console.log("Previous condition was 0");
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
    }
    // If the last move was a load
    else if (data[prevStep]["condition"] == "1") {
        const prevDestinationContainer = document.getElementById(prevDestination);
        prevDestinationContainer.style.backgroundColor = "white";
    }
    // If the last move was an unload
    else if (data[prevStep]["condition"] == "2") {
        const prevDestinationContainer = document.getElementById(prevDestination);
        prevDestinationContainer.style.backgroundColor = "white";

        prevDestinationContainer.children[1].textContent = "{00000}";
        prevDestinationContainer.children[2].textContent = "UNUSED";
    }
    // You can combine the previous two conditionals for cleanliness
    

    // Get the next operation and pass it into the highlight function
    // In a try block because it will eventually reach the end of the data object
    try {
        var condition = data[currentStep]["condition"];
        var destination = data[currentStep]["destination"];
        console.log("destination");
        console.log(destination);
        
        if (condition == "0") {
            var origin = data[currentStep]["origin"];
            highlightCurrentOperation(origin, destination);
        }
        else if (condition == "1") {
            highlightCurrentLoad(destination);
        }
        else if (condition == "2") {
            highlightCurrentUnload(destination);
        }    
    } catch (error) {
        // We reached the end and can now proceed in our direction
        console.log("Reached end of the data object");
        
        // TODO IMPLEMENT THE NEXT STEP IN THE PROCESS
        
        // Create a new object that will contain the final manifest information on the screen
        newManifest = new Object();
        for (let i = 0; i < containerButtonArr.length; i++) {
            var containerPosition = containerButtonArr[i].children[0].id;
            var containerWeight = containerButtonArr[i].children[0].children[1].textContent;
            var containerDescription = containerButtonArr[i].children[0].children[2].textContent;
    
            var obj = new Object();
            // obj.position = containerPosition;
            obj.weight = containerWeight.slice(1, -1);
            obj.description = containerDescription;
    
            newManifest[containerPosition] = obj;        
        }

        console.log("newManifest:");
        console.log(newManifest);
        console.log(urlForExportManifest);
        newManifestJson = JSON.stringify(newManifest);

        // Send this new manifest data to the python side to trigger a download and redirect to home page
        fetch(urlForExportManifest, {
            method: 'POST',
            credentials: "include",
            body: newManifestJson,
            cache: "no-cache",
            redirect: "follow",
            headers: new Headers({
                "content-type": "application/json"
            })
        })
        .then(response => {
            // Grab redirect link and follow through with it
            if(response.redirected){
                window.location.href = response.url;
            }
        })
        .catch(function(err) {
            console.info(err + " url: " + url);
        });
    }
}

// TODO: Here we should hide/show a graphic at the top that says what to do with the green and red containers
function highlightCurrentOperation(origin, destination) {
    const originContainer = document.getElementById(origin);
    const destinationContainer = document.getElementById(destination);

    originContainer.style.backgroundColor = "green";
    destinationContainer.style.backgroundColor = "red";
}

// TODO: Here we should hide/show a graphic at the top that says to load into the green container
function highlightCurrentLoad(destination) {   
    console.log("destination value inside highlightCurrentLoad");
    console.log(destination);
    
    // Bring up the information collection modal
    informationModal = document.getElementById("informationInputContainer");
    informationModal.style.display = "flex";

    // Add a listener to the submit button to check when they are satisfied
    // console.log("Checking current step");
    // console.log(currentStep);
    if (currentStep == 1) {
        inputSubmitButton = document.getElementById("inputSubmitButton");
        inputSubmitButton.addEventListener("click", collectInputInformation);
        inputSubmitButton.destination = destination;
    }
    else {
        // inputSubmitButton = document.getElementById("inputSubmitButton");
        // inputSubmitButton.removeEventListener("click", collectInputInformation);
        // inputSubmitButton.addEventListener("click", collectInputInformation);
        inputSubmitButton.destination = destination;
    }

    // const destinationContainer = document.getElementById(destination);
    // destinationContainer.style.backgroundColor = "green";

    function collectInputInformation(evt) {
        // TODO: Add a check if the information is empty/legal
        destination = evt.currentTarget.destination;

        destinationContainer = document.getElementById(destination);
        destinationContainer.style.backgroundColor = "green";

        nameInput = document.getElementById("nameInput");
        weightInput = document.getElementById("weightInput");
        descriptionInput = document.getElementById("descriptionInput");
        
        nameVal = nameInput.value;
        console.log("nameVal");
        console.log(nameVal);
        weightVal = weightInput.value;
        descriptionVal = descriptionInput.value;
        
        console.log("destination value inside collectInputInformation");
        console.log(destination);
        
        destinationContainer.children[1].textContent = "{" + (parseInt(weightVal)).toLocaleString('en-US', {minimumIntegerDigits: 5, useGrouping:false}) + "}";
        destinationContainer.children[2].textContent = nameVal;
        
        informationModal.style.display = "none";
        nameInput.value = "";
        weightInput.value = "";
        descriptionInput.value = "";
    }
}

// TODO: Here we should hide/show a graphic at the top that says to unload the green container
function highlightCurrentUnload(destination) {
    const destinationContainer = document.getElementById(destination);

    destinationContainer.style.backgroundColor = "green";
}