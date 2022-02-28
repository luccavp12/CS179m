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

    for (let i = 0; i < positionList.length; i++) {
        for (let j = 0; j < containerButtonArr.length; j++) {
            // Trying to retrieve all the information about the container being changed
            // if the current container to be changed is found in the full list of containers (with container details)
            if (positionList[i] == containerButtonArr[j].children[0].id) {
                var containerPosition = containerButtonArr[j].children[0].id;
                var containerWeight = containerButtonArr[j].children[0].children[1].textContent;
                var containerDescription = containerButtonArr[j].children[0].children[2].textContent;

                var obj = new Object();
                // obj.position = containerPosition;
                obj.weight = containerWeight.slice(1, -1);
                obj.description = containerDescription;
                obj.loadUnload = loadUnloadBool[i];

                changeList[containerPosition] = obj;
                
                console.log(obj);
            }
        }
    }

    console.log(changeList);
    var changeListJson = JSON.stringify(changeList);
    console.log(changeListJson);

    // console.log(urlForAlgo);
    // var request = new XMLHttpRequest();
    // request.open('POST', urlForAlgo); // Might have to include |tojson
    // // console.log(this);
    // request.send(changeListJson);

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
        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });    
}

function checkIfLoad() {
    console.log("Inside checkIfLoad");

    // var data = JSON.parse(this.responseText);
    // console.log(data);
}