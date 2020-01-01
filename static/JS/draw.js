// This file allows the user to draw in the canvas box



// Define the drawing variable. Action = Draw if drawing = true
var drawing = false;
// Context of the canvas
var context;
// Offsets of the box
var offset_left = 0;
var offset_top = 0;


// Initialization function: This function will run automatically when the page is loading
function start_canvas ()
{
    // Hide the Try Again button
    document.getElementById("try_again").style.display = "none";
    // Get the canvas and its context
    var canvas = document.getElementById ("canvas");
    context = canvas.getContext ("2d");
    // Define actions corresponding to events
    canvas.onmousedown = function (event) {mousedown(event)};
    canvas.onmousemove = function (event) {mousemove(event)};
    canvas.onmouseup   = function (event) {mouseup(event)};
    for (var o = canvas; o ; o = o.offsetParent) {
    offset_left += (o.offsetLeft - o.scrollLeft);
    offset_top  += (o.offsetTop - o.scrollTop);
    }
    draw();
}


// Get the position of the mouse
function getPosition(evt)
{
    evt = (evt) ?  evt : ((event) ? event : null);
    // left and top represent the positions x and y
    var left = 0;
    var top = 0;
    var canvas = document.getElementById("canvas");
    // get the offsets (with potential scroll)
    if (evt.pageX) {
    left = evt.pageX;
    top  = evt.pageY;
    } else if (document.documentElement.scrollLeft) {
    left = evt.clientX + document.documentElement.scrollLeft;
    top  = evt.clientY + document.documentElement.scrollTop;
    } else  {
    left = evt.clientX + document.body.scrollLeft;
    top  = evt.clientY + document.body.scrollTop;
    }
    left -= offset_left;
    top -= offset_top;

    return {x : left, y : top}; 
}


// Action function
function mousedown(event)
{
    drawing = true;
    var location = getPosition(event);
    context.lineWidth = 12.0;
    context.strokeStyle="#000000";
    context.beginPath();
    context.moveTo(location.x,location.y);
}


// Action function
function mousemove(event)
{
    if (!drawing) 
        return;
    var location = getPosition(event);
    context.lineTo(location.x,location.y);
    context.stroke();
}


// Action function
function mouseup(event)
{
    if (!drawing) 
        return;
    mousemove(event);
    drawing = false;
}


// Define the color and the canvas size
function draw()
{
    context.fillStyle = '#ffffff';
    context.fillRect(0, 0, 420, 420);
}


// Clear the canvas when the button is clicked
function clearCanvas()
{
    context.clearRect (0, 0, 420, 420);
    draw();
}


// Try again function running when the corresponding button is clicked
function try_again() {
    // We clear the canvas
    clearCanvas()
    // Display the 'clear' and 'predict it' buttons
    document.getElementById("clear").style.display = "";
    document.getElementById("pred").style.display = "";
    // Hide the prediction messages and the 'try again' button
    document.getElementById("message1").innerHTML = "";
    document.getElementById("message2").innerHTML = "";
    document.getElementById("try_again").style.display = "none";
}


// Predict function running when the corresponding button is clicked
function predict() {
    // Display two messages and hide the 'clear' and 'predict it' buttons
    document.getElementById("message1").innerHTML = "Predicting.";
    document.getElementById("message2").innerHTML = "Please wait a moment...";
    document.getElementById("clear").style.display = "none";
    document.getElementById("pred").style.display = "none";
    // Get the canvas and its data
    var canvas = document.getElementById ("canvas");
    var imageData =  canvas.toDataURL('image/png');
    // Call a function to make the prediction
    $.ajax({
        type: "POST",
		url: "/hidden",
		data:{
			imageBase64: imageData
        }
    }).done(function(response) {
        // When the function is done, display the results
        console.log(response);
        var response = JSON.parse(response)
		document.getElementById("try_again").style.display = "";
        document.getElementById("message1").innerHTML = "Prediction:";
        document.getElementById("message2").innerHTML = response['result'];
        });
}


// When the page is loaded, the initialization function runs
onload = start_canvas;