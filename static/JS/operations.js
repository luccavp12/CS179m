// This is the change list json object to be filled and sent to the backend
var changeList = new Object();

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
const containerButtonArr = document.getElementsByClassName("containerButtonContainer")

// Loop through the list of all container buttons, and set event listeners on all of container buttons
for (var i = 0; i < containerButtonArr.length; i++) {
    containerButtonArr[i].addEventListener('click', containerSelection);
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
            console.log("Can be bundled and sent to json");
        }
    }
    // If a container button is clicked AND the user is in unloading mode
    else if (selectedMode == 2) {
        // if the container button that is clicked is the proper button and a container in the location
        if (containerDescription != "NAN" || containerDescription != "UNUSED") {
            // Take the container information and send it to the Changes.json
            console.log("Can be bundled and sent to json");
        }
    }
}

var object1012 = new Object();
object1012.description = "box of farts"
object1012.weight = 100;

console.log(object1012);

console.log(JSON.stringify(object1012));