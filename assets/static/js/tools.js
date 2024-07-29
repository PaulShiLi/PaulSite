// Make textarea autogrow
function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function copy(commonType) {
    // Get the text field
    var copyText = document.getElementById(`resultContent_${commonType}`);
    
     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.innerText);
}
  

// Add listeners for buttons
function encodeToggle(commonType) {
    var encodeButton = document.getElementById(`encodeButton_${commonType}`);
    var decodeButton = document.getElementById(`decodeButton_${commonType}`);
    // Change button bold
    decodeButton.classList.remove('active');
    encodeButton.classList.add('active');
}

function decodeToggle(commonType) {
    var decodeButton = document.getElementById(`decodeButton_${commonType}`);
    var encodeButton = document.getElementById(`encodeButton_${commonType}`);
    // Change button bold
    encodeButton.classList.remove('active');
    decodeButton.classList.add('active');
}

function submitToggle(commonType) {
    if (commonType == "b64") {
        var decodeButton = document.getElementById(`decodeButton_${commonType}`);
        var encodeButton = document.getElementById(`encodeButton_${commonType}`);
        var content = document.getElementById(`input_${commonType}`)
        var result = document.getElementById(`result_${commonType}`)
        var resultContent = document.getElementById(`resultContent_${commonType}`)
        if (decodeButton.classList.contains("active")) {
            resultContent.innerText = atob(content.value);
        }
        else {
            resultContent.innerText = btoa(content.value);
        }
        // Remove hidden attribute in result
        result.removeAttribute("hidden");
    }
}
